# -*- coding: utf-8 -*-
"""DaSh-8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12lZ-Sw_B5KXinYIJb9707w96WfYi_kin
"""

import pandas as pd
import requests
from datetime import datetime, timedelta

def get_weather_data(api_key, city):
    base_url =  "http://api.openweathermap.org/data/2.5/forecast"    #f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'  #"http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # You can change this to 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    #response = requests.get(base_url)
    d = response.json()

    if response.status_code == 200:
        #print(d['list'])
        return [d['list'], d['city']['population']]
        #print(d)
        #return d
    else:
        print(f"Failed to retrieve data for {city}")
        return None

def get_average_temperature(weather_data):
    #print('weather_data', weather_data)
    temperatures = [entry['main']['temp'] for entry in weather_data]
    #print('temperatures', temperatures)
    #print (sum(temperatures))
    #print (len(temperatures))
    return sum(temperatures) / len(temperatures)

def main():
    api_key = '722ef9fd22420b8a16fe4be923918a3d'
    #cities_file = 'cities.csv'

    # Read cities from CSV file
    cities_df = pd.read_excel("city_data_bi_developer_case_study_final (1).xlsx", sheet_name="raw_city_data")

    top_cities_df = cities_df.sort_values(by='Elevation(m)', ascending=False).head(10)

    #cities_df = pd.read_csv(cities_file)
    #cities = cities_df['City'].tolist()

    out_list_list = []

    for i in top_cities_df.index:
        #print("\n\n")

        lat = cities_df.at[i, "Latitude"]
        lon = cities_df.at[i, "Longitude"]
        city = cities_df.at[i, "City"]
        Country = cities_df.at[i, "Country"]
        language = cities_df.at[i, "Language"]
        climate = cities_df.at[i, "Climate"]
        population_csv = cities_df.at[i, "Population"]




        weather_data, population_api = get_weather_data(api_key, city)


        if weather_data:
            # Get weather data for the next five days
            today = datetime.now()
             #next_five_days = [today + timedelta(days=i) for i in range(5)]

            next_five_days = []
            for i in range(5):
                next_five_days.append(today + timedelta(days=i))
            #print('next_five_days', next_five_days)



                #print('day_data', day_data)
            #day_data = [entry for entry in weather_data if datetime.fromtimestamp(entry['dt']).date() == day.date()]

            day_data = []
            for day in next_five_days:
                for entry in weather_data:
                    if datetime.fromtimestamp(entry['dt']).date() == day.date():
                        day_data.append(entry)
                        break

            #print("day_data", day_data)
            #print(len(day_data))

            average_temp = get_average_temperature(day_data)
            population_diff = abs(population_csv-population_api)
            print(f"Date: {today}, City: {city}, Average Temperature: {average_temp:.2f}°C, Country: {Country}, Language: {language}, climate: {climate}, Population from csv: {population_csv}, population from API: {population_api}, population diff: {population_diff}")

            out_list_list.append([today, city, round(average_temp,2), Country, language, climate, population_csv, population_api, population_diff])




        else:
            print("No weather data")

    df_out = pd.DataFrame(out_list_list, columns=["Date", "City", "Average Temperature", "Country", "Language", "Climate", "Population from csv", "population from API", "population diff"])
    df_out.to_csv("Dash-8.csv", index=False)

if __name__ == "__main__":
    main()

