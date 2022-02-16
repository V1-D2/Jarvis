import pyowm
import geopy
from geopy.geocoders import Nominatim



def weatherIn(place):
    listOfWeather = weatherPl(place[0].upper()+place[1::-1])

    forecastInPlace = ("Сейчас тут " + str(listOfWeather["status"]) + " температура " + str(
    listOfWeather["temp"]["temp"]) + " градусов цельсия, влажность " + str(
        listOfWeather["humidity"]) + " процентов.")

    if (listOfWeather["willItBeRaine"] == True):
        forecastInPlace += (" В течении 3 часов должен быть дождь.")
    if (listOfWeather["willItBeSnowe"] == True):
            forecastInPlace += ("Более того в ближайшее время ожидается снег.")

    return forecastInPlace

def weather():
    listOfWeather = weatherPl("None")
    forecast = ("За окном " + str(listOfWeather["status"])+" температура "+str(listOfWeather["temp"]["temp"])+" градусов цельсия, влажность "+str(listOfWeather["humidity"])+" процентов. ")
    if(listOfWeather["willItBeRaine"] == True):
        forecast += ("В течении 3 часов должен быть дождь. ")
    if(listOfWeather["willItBeSnowe"] == True):
        forecast += ("Более того в ближайшее время ожидается снег.")
    return forecast

def weatherPl(place):
    # coordinates
    loc = f'{place}'
    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)

    lat = location.latitude
    lon = location.longitude

    #weather
    owm =  pyowm.OWM('626946db33980c9e9634d336ca33d650',language = "RU")

    observation = owm.weather_at_place(place)

    w = observation.get_weather()

    weather = {"status":w.get_detailed_status(),
               "temp":w.get_temperature('celsius'),
               "pressure":w.get_pressure(),
               "humidity":w.get_humidity(),
               "sunrise":w.get_sunrise_time(timeformat='iso')[11:][:8],
               "sunset":w.get_sunset_time(timeformat='iso')[11:][:8],
               "wind":w.get_wind()}

    fc = owm.three_hours_forecast_at_coords(lat, lon)
    rain = fc.will_have_rain()
    snow = fc.will_have_snow()
    rains = fc.when_rain()
    weather["willItBeRaine"] = rain
    weather["willItBeSnowe"] = snow
    #print(rains)
    return weather
    '''
    print(w.get_detailed_status())
    temp = w.get_temperature('celsius')['temp_max']
    print(w.get_pressure())
    print(w.get_rain())
    print(w.get_sunrise_time(timeformat='iso')[11:][:8])
    print('Температура в районе: ' + str(temp) + '°C')
    '''

#print(weather())