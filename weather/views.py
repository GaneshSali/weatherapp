import requests
from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City

def main(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():

            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            r = requests.get(url.format(new_city)).json()
            print(r)

            if r['cod'] == 200:
                if City.objects.filter(name=r['name'],weather_id=r['id']).exists():
                    err_msg = 'City already exists in the List!'

                else:
                    City.objects.create(name=r['name'],weather_id=r['id'])
            else:
                err_msg = 'City does not exist in the world!'
        
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
    else:
        form = CityForm()

    cities = City.objects.all().order_by('-id')

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }
    return render(request, 'weather/weather.html',context)


def delete_city(request, city):
    City.objects.get(name=city).delete()
    return redirect('weather')
