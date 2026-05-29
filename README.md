# Weather API App
### Live Current Conditions via OpenWeatherMap — ZIP Code or City/State Input

---

## Overview

A terminal-based Python program that retrieves and displays current weather conditions for any U.S. location. The user provides either a 5-digit ZIP code or a city and 2-letter state abbreviation, selects a temperature unit, and the program makes two successive API calls — first to resolve the location to coordinates, then to pull the current weather — before printing a formatted report.

---

## How It Works

| Step | What Happens | API Endpoint |
|---|---|---|
| **1. Geocoding** | ZIP code or city/state is resolved to latitude/longitude | `geo/1.0/zip` or `geo/1.0/direct` |
| **2. Weather Lookup** | Coordinates are sent to retrieve current conditions | `data/2.5/weather` |
| **3. Report** | Formatted weather summary is printed to the terminal | — |

---

## Features

- Accepts **5-digit ZIP code** or **city + 2-letter state abbreviation**
- Input validation at every prompt — ZIP regex, city name regex, and a full state-abbreviation checklist
- Temperature units: **Fahrenheit**, **Celsius**, or **Kelvin** (user's choice)
- Graceful error handling for HTTP errors, connection errors, and 404 responses
- Loop allows multiple lookups in a single session without restarting

---

## Sample Output

```
Marty's Fantastic API Weather App
---------------------------------

Weather Report for the city of Cleveland
-----------------------------------------------
Current weather:         Overcast clouds
Current temperature:     62°F
Feels like:              60°F
Current Min:             58°F
Current Max:             64°F
Pressure:                1015 hPa
Humidity:                72%
-----------------------------------------------
```

---

## Project Structure

```
weather-app/
│
└── weather_app.py      # Main program — all logic in a single self-contained script
```

---

## Requirements

```
requests
```

Install with:
```bash
pip install requests
```

Or using the requirements file:
```bash
pip install -r requirements.txt
```

---

## API Key Setup

This program uses the [OpenWeatherMap API](https://openweathermap.org/api). A free-tier account provides sufficient access. Register at [openweathermap.org](https://home.openweathermap.org/users/sign_up) to obtain a key.

The API key in the script has been replaced with a placeholder. Before running the program, open `weather_app.py` and substitute your own key on line 13:

```python
api_key = "your_api_key_here"   # <-- replace with your OpenWeatherMap API key
```

---

## Running the Program

```bash
python weather_app.py
```

The program is fully interactive — it will prompt you for all inputs at the terminal.

---

## Technologies

| Tool | Use |
|---|---|
| `requests` | HTTP calls to the OpenWeatherMap REST API |
| `re` | Input validation (ZIP format, city name, state abbreviation) |
| OpenWeatherMap Geocoding API | Resolves ZIP or city/state to lat/lon |
| OpenWeatherMap Current Weather API | Retrieves conditions from coordinates |

---

## Academic Context

This project was developed as the **final project for DSC 510** (Introduction to Programming, master's level). The assignment required building a complete, multi-function Python program that integrates an external REST API, validates user input, handles errors, and produces formatted output — demonstrating core programming competencies in functions, loops, exception handling, regex, and JSON parsing.

---

*API: [OpenWeatherMap Current Weather Data](https://openweathermap.org/current) — free tier. Program written August 2023.*
