import requests

response = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=39.10&longitude=-84.51&current_weather=true"
)

data = response.json()

print("Current weather in Cincinnati:")
print (data)

print("pulled out values:")
print("temperature:" , data ["current_weather"]["temperature"])
print("windspeed:" , data ["current_weather"]["windspeed"])

response2 = requests.post("https://httpbin.org/post",
    json={
        "material": "stainless_steel",
        "height": 10,
        "width": 4,
        "weld_type": "corrosion_resistant"
    }
)

data2 = response2.json()

print ("Response from POST request:")
print("Staus code:", response2.status_code)
print("What server received:", data2["json"])