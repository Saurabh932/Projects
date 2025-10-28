import requests
import json

class WeatherApp:
    def __init__(self):
        self.weather = []


    def temperature(self, city):
        # clear previous data each time a new city is searched
        self.weather.clear()
        
        api_key = "69d6138c430045dfb33130437252810"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        
        req = requests.get(url)
        wdict = json.loads(req.text)

        temp = wdict['current']["temp_c"]
        ctext = wdict["current"]["condition"]["text"]
        cicon = wdict["current"]["condition"]['icon']
        
        if temp < 10:
            feels = "Cold 🧥"
        elif 10 <= temp <= 25:
            feels = "Pleasant 🌤️"
        else:
            feels = "Hot ☀️"

        # ✅ Store values in list
        self.weather.extend([temp, ctext, cicon, feels])
        
        return self.weather
        # return status
        
    def view_temperature(self):
        return self.weather
        
        
if __name__=="__main__":
    weather = WeatherApp()
    weather.temperature("Nagpur")
    print(weather.view_temperature())