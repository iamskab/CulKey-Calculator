from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .forms import *
import requests
import json
from datetime import date
# Create your views here.

def convert24(str1):

    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        return str(int(str1[:2]) + 12) + str1[2:8]



def time_difference(time_start, time_end):

    start = datetime.strptime(time_start, "%H%M")
    end = datetime.strptime(time_end, "%H%M")
    difference = end - start
    minutes = difference.total_seconds() / 60
    return int(minutes)

def add_time(time_start, minutes):

    start = datetime.strptime(time_start, "%H%M")
    end = start + timedelta(minutes=minutes)
    return end

def geo(request):
    form = Locationform(request.POST or None)

    if request.method == 'POST':
       if request.POST.get('ajax_check') == "True":
         if form.is_valid():
            key = form.cleaned_data
            city = key.get('Enter_your_location')
            url = 'https://weather.cit.api.here.com/weather/1.0/report.json'

            parameters = dict(
                product='forecast_astronomy',
                name=city,
                app_id='cTqOSjbtmgQB1XGtr5SB',
                app_code='9tCOayrEASzoc6cLYeK_wQ'
            )

            response = requests.get(url=url, params=parameters)
            data = response.json()

            x = "Type" in data
            if x == True:
                return HttpResponse("No City Found")
            else:
                print(data)

                date_details = data['feedCreation']
                year = int(date_details[0:4])
                month = int(date_details[5:7])
                date_num = int(date_details[8:10])
                week_day = date(year, month, date_num).weekday()
                if week_day==0 :
                    gulika = 6
                    raahu = 2
                    yama = 4
                elif week_day==1 :
                    gulika = 5
                    raahu = 7
                    yama = 3
                elif week_day==2 :
                    gulika = 4
                    raahu = 5
                    yama = 2
                elif week_day==3 :
                    gulika = 3
                    raahu = 6
                    yama = 1
                elif week_day==4 :
                    gulika = 2
                    raahu = 4
                    yama = 8
                elif week_day==5 :
                    gulika = 1
                    raahu = 3
                    yama = 7
                else :
                    gulika = 7
                    raahu = 8
                    yama = 5

                sunrise = data['astronomy']['astronomy'][0]['sunrise'][0:4]
                sunset = data['astronomy']['astronomy'][0]['sunset'][0:4]
                sunrise = "0"+sunrise+":00 "+data['astronomy']['astronomy'][0]['sunrise'][4:6]
                sunset = "0"+sunset+":00 "+data['astronomy']['astronomy'][0]['sunset'][4:6]
                sunrise = convert24(sunrise)
                sunset = convert24(sunset)
                sunrise = sunrise[0:2]+sunrise[3:5]
                sunset = sunset[0:2] + sunset[3:5]

                time_diff = time_difference(sunrise,sunset)
                time_unit_diff = time_diff/8

                raahu_kaala_start = add_time(sunrise,(raahu-1)*time_unit_diff).time()
                raahu_kaala_end = add_time(sunrise,(raahu)*time_unit_diff).time()

                yama_kaala_start = add_time(sunrise, (yama - 1) * time_unit_diff).time()
                yama_kaala_end = add_time(sunrise, (yama) * time_unit_diff).time()

                gulika_kaala_start = add_time(sunrise, (gulika - 1) * time_unit_diff).time()
                gulika_kaala_end = add_time(sunrise, (gulika) * time_unit_diff).time()

                yama_kaala_start = yama_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                yama_kaala_end = yama_kaala_end.strftime("%H:%M:%S.%f")[0:8]
                gulika_kaala_start = gulika_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                gulika_kaala_end = gulika_kaala_end.strftime("%H:%M:%S.%f")[0:8]
                raahu_kaala_start = raahu_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                raahu_kaala_end = raahu_kaala_end.strftime("%H:%M:%S.%f")[0:8]

                return HttpResponse(json.dumps({
                    'sunrise': data['astronomy']['astronomy'][0]['sunrise'],
                    'sunset': data['astronomy']['astronomy'][0]['sunset'],
                    'moonrise': data['astronomy']['astronomy'][0]['moonrise'],
                    'moonset': data['astronomy']['astronomy'][0]['moonset'],
                    'country': data['astronomy']['country'],
                    'state': data['astronomy']['state'],
                    'timezone': data['astronomy']['timezone'],
                    'latitude': data['astronomy']['latitude'],
                    'longitude': data['astronomy']['longitude'],
                    'date': data['feedCreation'][0:10],
                    'raahu_kaala_s': raahu_kaala_start,
                    'raahu_kaala_e': raahu_kaala_end,
                    'gulika_kaala_s': gulika_kaala_start,
                    'gulika_kaala_e': gulika_kaala_end,
                    'yama_kaala_s': yama_kaala_start,
                    'yama_kaala_e': yama_kaala_end,
                }))

    return render(request, 'cal/geo.html', {'form': form, })