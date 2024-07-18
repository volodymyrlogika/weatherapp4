from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatIconButton
import requests

from settings import API_KEY, WEATHER_URL, FORECAST_URL

class WeatherCard(MDCard):
    def __init__(self, date, image, temp, temp_like, desc, wind_speed, humidity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_time.text = date
        self.ids.image.source = f'https://openweathermap.org/img/wn/{image}@2x.png'
        self.ids.temp.text = f'{temp} °C'
        self.ids.temp_like.text = f'Відчувається як {temp_like} °C'
        self.ids.desc.text = desc.capitalize()
        self.ids.wind_speed.text = f'Швидкість вітру: {wind_speed} м/c'
        self.ids.humidity.text = f'Вологість: {humidity}%'


class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_weather_data(self, url, city):
        """Функція робить запит до сайту погоди і повертає JSON файл з результатом"""
        api_params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(url, api_params)
        response = data.json()
        print(response)
        return response

    def create_weather_card(self, data):
        icon = data["weather"][0]["icon"]
        desc =  data["weather"][0]["description"]
        temp = data["main"]["temp"]
        temp_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        if 'dt_txt' in data:
            date = data["dt_txt"][5:-3]
        else:
            date = "Зараз"
        new_card = WeatherCard(date, icon, temp, temp_like, desc, wind_speed, humidity)
        self.ids.weather_carousel.add_widget(new_card)

    def search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_name.text.lower().strip()
        print(city)
        current_weather = self.get_weather_data(WEATHER_URL, city)
        self.create_weather_card(current_weather)

        forecast = self.get_weather_data(FORECAST_URL, city)
        for period in forecast["list"]:
            self.create_weather_card(period)



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Builder.load_file("style.kv")
        self.screen = HomeScreen(name="home")
        return  self.screen


MainApp().run()