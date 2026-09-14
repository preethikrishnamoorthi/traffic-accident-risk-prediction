import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Number_of_Vehicles": 2,
    "Number_of_Casualties": 1,
    "Day_of_Week": 2,
    "Hour": 18,
    "Road_Type": "Single carriageway",
    "Speed_limit": 60,
    "Junction_Control": "Give way or uncontrolled",
    "Light_Conditions": "Daylight: Street light present",
    "Weather_Conditions": "Fine without high winds",
    "Road_Surface_Conditions": "Dry",
    "Urban_or_Rural_Area": "Urban",
    "Latitude": 51.5,
    "Longitude": -0.1,
    "Year": 2020
}

response = requests.post(url, json=data)

print(response.json())