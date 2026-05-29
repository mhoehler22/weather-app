# DSC 510 - Final Project
# Programming Assignment - Final
# Author Martin Hoehler
# 8/12/2023
# Weather API: A program that will ask the user for location info, (either a zipcode, or a city/state combo), and call
# the openweathermap.org API to determine latitude and longitude coordinates.  It will then call an API with those
# coordinates to retrieve the current weather.  Finally, it will print a current weather report using the user's
# preferred unit for temperatures.

import requests
import re

api_key = "your_api_key_here"


def zip_API(zip_code):
    # Function to take an inputted zipcode, look it up via API, and return latitude and longitude coordinates.
    zip_url = "https://api.openweathermap.org/geo/1.0/zip"
    querystring = {"zip": zip_code, "APPID": api_key}
    headers = {'cache=control': 'no-cache'}
    try:
        # Try block to test the API with exceptions for HTTP Error and Connection Error
        zip_find = requests.get(zip_url, headers=headers, params=querystring)
    except requests.HTTPError as e:
        print("There was an HTTP error:  \n", e, "\n")
    except requests.ConnectionError as e:
        print("There was a connection error: \n", e, "\n")
    else:
        if zip_find.status_code == 404:
            # This check handles 5-digit numbers that aren't on the zipcode list.
            print("That zipcode wasn't found.")
            lat = None
            lon = None
            return lat, lon
        elif len(zip_find.json()) == 0:
            # This check handles "IndexError: list index out of range" errors.
            print("That zipcode wasn't found.")
            lat = None
            lon = None
            return lat, lon
        else:
            # If the API executes without issue, we convert to JSON and extract the latitude and longitude.
            zip_find_JSON = zip_find.json()
            lat = zip_find_JSON['lat']
            lon = zip_find_JSON['lon']
            return lat, lon


def city_API(location):
    # Function to take an inputted city/state combo, look it up via API, and return latitude and longitude coordinates.
    city_url = "https://api.openweathermap.org/geo/1.0/direct"
    querystring_city = {"q": location.strip(), "APPID": api_key}
    # We allow spaces in "location", so we need to use strip() here to make sure there's no leading or ending spaces.
    headers = {'cache=control': 'no-cache'}
    try:
        # Try block to test the API with exceptions for HTTP Error and Connection Error
        city_find = requests.get(city_url, headers=headers, params=querystring_city)
    except requests.HTTPError as e:
        print("There was an HTTP error:  \n", e, "\n")
    except requests.ConnectionError as e:
        print("There was a connection error: \n", e, "\n")
    else:
        if city_find.status_code == 404:
            # This check handles 404 errors from cities not on the list.
            print("That city/state combination wasn't found.")
            lat = None
            lon = None
            return lat, lon
        elif len(city_find.json()) == 0:
            # This check handles "IndexError: list index out of range" errors.
            print("That city/state combination wasn't found.")
            lat = None
            lon = None
            return lat, lon
        else:
            # If the API executes without issue, we convert to JSON and extract the latitude and longitude.
            city_find_list = city_find.json()
            city_find_JSON = city_find_list[0]
            lat = city_find_JSON['lat']
            lon = city_find_JSON['lon']
            return lat, lon


def weather_API(lat, lon, units):
    # Function to take input latitude and longitude coordinates and units preferred for temperature.
    # Next, it will look up via API and return weather JSON data.
    current_weather = None
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    if units == "imperial":
        querystring_city = {"lat": lat, "lon": lon, "units": "imperial", "APPID": api_key}
    elif units == "metric":
        querystring_city = {"lat": lat, "lon": lon, "units": "metric", "APPID": api_key}
    else:
        querystring_city = {"lat": lat, "lon": lon, "APPID": api_key}
    headers = {'cache=control': 'no-cache'}
    try:
        # Try block to test the API with exceptions for HTTP Error and Connection Error
        weather_find = requests.get(weather_url, headers=headers, params=querystring_city)
    except requests.HTTPError as e:
        print("There was an HTTP error:  \n", e, "\n")
    except requests.ConnectionError as e:
        print("There was a connection error: \n", e, "\n")
    else:
        if weather_find.status_code == 404:
            print("Error:  Latitude and Longitude not found.  Please try again.")
        else:
            current_weather = weather_find.json()
    return current_weather


def weather_report(weather, units):
    # Function to print a weather report based on the JSON data returned by the weather_API() function.
    # Also brings in preferred units for temperature.
    degree_symbol = u'\N{DEGREE SIGN}'
    # Degree symbol code found: https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
    print("\nWeather Report for the city of", weather['name'],
          "\n-----------------------------------------------")
    if units == "imperial":
        degree_letter = "F"
    elif units == "metric":
        degree_letter = "C"
    else:
        degree_letter = "K"
    description_list = weather['weather']
    description = [a_dict['description'] for a_dict in description_list]
    main_dict = weather['main']
    temp = main_dict['temp']
    feels = main_dict['feels_like']
    temp_min = main_dict['temp_min']
    temp_max = main_dict['temp_max']
    pressure = main_dict['pressure']
    humidity = main_dict['humidity']
    print("Current weather:        ", description[0].capitalize())
    print("Current temperature:     {}{}{}".format(temp, degree_symbol, degree_letter))
    print("Feels like:              {}{}{}".format(feels, degree_symbol, degree_letter))
    print("Current Min:             {}{}{}".format(temp_min, degree_symbol, degree_letter))
    print("Current Max:             {}{}{}".format(temp_max, degree_symbol, degree_letter))
    print("Pressure:                {} hPa".format(pressure))
    print("Humidity:                {}%".format(humidity))
    print("-----------------------------------------------")


def main():
    # User interface, allows user to choose between inputting a city or a zipcode.
    print("\nMarty's Fantastic API Weather App"
          "\n---------------------------------\n")
    repeat_answer = input("Would you like to know the weather in your area?  ('y' to continue, 'q' to quit) >> ")
    while repeat_answer.lower() != 'q':
        if repeat_answer.lower() != 'y':
            repeat_answer = input("That wasn't one of the choices.  Try again.  ('y to continue, 'q' to quit) >> ")
        else:
            deg_answer = input("\nWould you like temperatures in Fahrenheit ('f'), Celsius ('c') or Kelvin ('k')? >> ")
            while deg_answer.lower() != 'f' and deg_answer.lower() != 'c' and deg_answer.lower() != 'k':
                print("\nThat wasn't one of the choices.")
                deg_answer = input(
                    "\nWould you like temperatures in Fahrenheit ('f'), Celsius ('c') or Kelvin ('k')? >> ")
            else:
                if deg_answer.lower() == 'f':
                    units = "imperial"
                elif deg_answer.lower() == 'c':
                    units = "metric"
                else:
                    units = "Kelvin"
            geo_answer = input("\nWould you like to look up the weather by zip code ('z') or city ('c')? >> ")
            while geo_answer.lower() != 'z' and geo_answer.lower() != 'c':
                geo_answer = input("That wasn't one of the choices.  Try again.  ('z' for zipcode, 'c' for city.) >> ")
            else:
                if geo_answer.lower() == "z":
                    zip_code = input("Please enter a 5 digit zip code. >> ")
                    while not re.match(r"^\d{5}$", zip_code):
                        # This regex will confirm that the zipcode is 5 digits.
                        if re.match(r"^\d{5}-\d{4}$", zip_code) or re.match(r"^\d{9}$", zip_code):
                            # This regex will look for 9-digit zipcodes and remind them to use 5-digit instead.
                            print("\nSorry, we cannot accommodate 9-digit zipcodes.")
                            zip_code = input("5-digit zip codes only.  Please try again. >> ")
                        else:
                            zip_code = input("\n5-digit zipcodes only.  Please try again. >> ")
                    else:
                        # if zip_code input passes through the regex match tests, we'll make the API call.
                        lat_lon = zip_API(zip_code)
                else:
                    # this branch is for when the user chooses 'c' to input a city.
                    city = input("Please type in your city. >> ")
                    while not re.match(r"^[a-zA-Z -]{2,}$", city):
                        # Regex to confirm city name is all letters, spaces or hyphens.  Excludes 1-letter words.
                        city = input("City name was invalid.  Please try again. >> ")
                    state = input("Please type in your state. (Two-letter abbreviation) >> ")
                    while not re.match(r"(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|"
                                       r"O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY])", state.upper()):
                        # regex for states: https://regex101.com/r/0y0X2q/1
                        state = input("Not a valid state abbreviation.  Please try again. >> ")
                    # If city and state pass the regex tests, it is combined with "USA" to create the location code
                    # that is fed into the city_API.
                    location = "{}, {}, USA".format(city, state)
                    lat_lon = city_API(location)

            lat = lat_lon[0]
            lon = lat_lon[1]
            if lat is not None and lon is not None:
                # This check for "None" in lat and lon will keep the code from proceeding to look up the weather in
                # instances where an error or exception was thrown when looking up lon and lat coordinates.
                # In the event of an error or exception, the code will jump past the weather API call and report
                # to allow the user to try again.
                weather = weather_API(lat, lon, units)
                weather_report(weather, units)
            repeat_answer = input("\nWould you like to look up another location? "
                                  "('y' to continue, 'q' to quit) >> ")
    else:
        # End code if user selects "q".
        print("\n------------------------------------------------------")
        print("\nThank you for using Marty's Fantastic API weather app.")
        print("\n------------------------------------------------------")


if __name__ == '__main__':
    main()
