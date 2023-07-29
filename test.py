import requests
response = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?q=москва&lang=ru&units=metric&appid=56a1127e15eec70e9830ad373111e01c")
data = response.json()
city = data["name"]

print(data["weather"][0]["main"])
