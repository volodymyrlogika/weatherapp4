from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatIconButton
import requests

from settings import API_KEY, WEATHER_URL

class WeatherCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

    def search(self):
        city = self.ids.city_name.text.lower().strip()
        print(city)
        current_weather = self.get_weather_data(WEATHER_URL, city)
        temp = current_weather["main"]["temp"]
        self.ids.content_text.text = f'{temp}°C'


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        Builder.load_file("style.kv")
        self.screen = HomeScreen(name="home")
        return  self.screen


MainApp().run()