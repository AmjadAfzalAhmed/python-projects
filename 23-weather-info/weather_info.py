from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout
from api_key import my_key
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# PyQt6 Widgets
class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.api_key = my_key
        self.submit.clicked.connect(self.search_click)

    # PyQt6 Widgets Settings
    def settings(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(250, 250, 500, 300)
    # PyQt6 Widgets UI
    def initUI(self):
        self.title = QLabel("Weather App")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter City Name")

        self.output = QLabel("Weather in your City")
        self.submit = QPushButton("Search")

        self.master = QVBoxLayout()
        self.master.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.master.addWidget(self.input_box)
        self.master.addWidget(self.submit)
        self.master.addWidget(self.output)

        self.setLayout(self.master)

    # PyQt6 Widgets Functions
    def search_click(self):
        self.results = self.get_weather(self.api_key, self.input_box.text())
        self.output.setText(self.results)
    # PyQt6 Widgets Functions
    def get_weather(self, api_key, city, country=""):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {'q': f"{city},{country}", 'appid': api_key, 'units': 'metric'}  # Added units for Celsius

        try:
            # API Request
            res = requests.get(base_url, params=params)
            data = res.json() # API Response
            
            # API Response
            if res.status_code == 200:
                city = data['name']
                country = data['sys']['country']
                temp_celsius = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                wind_direction = data['wind']['deg']
                # Weather Information
                weather_info = (f"Weather in {city}, {country}:\n"
                                f"Temperature: {temp_celsius:.2f}°C\n"
                                f"Weather: {weather_desc}\n"
                                f"Humidity: {humidity}%\n"
                                f"Wind Speed: {wind_speed} m/s\n"
                                f"Wind Direction: {wind_direction}°\n")
                return weather_info
            else:
                # API Error
                return f"Error: {data.get('message', 'Unknown error')}"
        except Exception as e:
            # Exception Error
            return f"Error: {e}"

if __name__ == "__main__":
    # PyQt6 Widgets
    app = QApplication([])
    main = Home() 
    main.show()
    app.exec()
