from django.shortcuts import render
import requests
from time import gmtime, strftime
from datetime import datetime


# Create your views here.

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'delhi'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7d2be569d05b6bba71af22167930d2f5'
    PARAMS = {'units':'metric'}
    
    response = requests.get(url,PARAMS)
    if response.status_code == 200:

    
        data = requests.get(url, PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        windsp = data['wind']['speed']
        name = data['name']
        sunset_unix = data['sys']['sunset']
        sunrise_unix = data['sys']['sunrise']

        day = datetime.now().date()
        formatted_sunset = get_sun_time(sunset_unix, timezone='Asia/Kolkata')
        formatted_sunrise = get_sun_time(sunrise_unix, timezone='Asia/Kolkata')

        #sunset_time = datetime.fromtimestamp(sunset_unix)

    # Format the datetime to 12-hour clock with AM/PM
        #sunset_12hr_format = sunset_time.strftime("%I:%M %p")

        return render(request, 'index.html',{'description':description, 'icon':icon, 'temp':temp, 'city':city, 'day':day, 'name':name,
        'humidity':humidity, 'pressure':pressure, 'windsp':windsp, 'temp_min':temp_min, 'temp_max':temp_max,
        'formatted_sunset': formatted_sunset, 'formatted_sunrise': formatted_sunrise})
    else:
        error_message = "City is not available"
        return render(request,'index.html',{'error_message':error_message})



import pytz


def get_sun_time(unix_timestamp, timezone='UTC'):
    # Convert UNIX timestamp to a datetime object
    dt = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.UTC)
    # Convert to the desired timezone
    local_dt = dt.astimezone(pytz.timezone(timezone))
    # Format the time in 12-hour format
    return local_dt.strftime('%I:%M %p')

