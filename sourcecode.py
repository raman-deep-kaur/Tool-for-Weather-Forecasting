import requests
import json
import tkinter as tk
import webbrowser

API_KEY = "17d59437ed32af4dce8429118c2d9b5d"  # Replace with your OpenWeatherMap API key

def get_weather(city):
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response_current = requests.get(current_weather_url)
    response_forecast = requests.get(forecast_url)

    if response_current.status_code == 200 and response_forecast.status_code == 200:
        current_weather_data = json.loads(response_current.text)
        forecast_data = json.loads(response_forecast.text)
        return current_weather_data, forecast_data
    else:
        print(f"Error: {response_current.status_code} - {response_forecast.status_code}")
        return None, None

def generate_html(current_weather, forecast):
    if current_weather is None or forecast is None:
        return

    city = current_weather['name']
    temperature = current_weather['main']['temp']
    humidity = current_weather['main']['humidity']
    description = current_weather['weather'][0]['description']

    html_content = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                overflow-x: hidden;
                width: 100vw;
                height: 100vh;
            }}
            .main {{
                margin-top: 50px;
            }}
            .weather-panel {{
                background-image: url(clear.jpg);
                background-size: cover;
                background-position: center;
                border-radius: 20px;
                box-shadow: 25px 25px 40px 0px rgba(0,0,0,0.33);
                color: #fff;
                overflow: hidden;
                position: relative;
                }}
          .weather-panel .header {{
              font-size: 24px;
              font-weight: bold;
              padding: 10px;
              background-color: rgba(0, 0, 0, 0.5);
              }}
             
            .weather-panel .data {{
            flex: 0 0 auto;
            padding: 10px;
            text-align: center;
            }}
            .weather-panel .info {{
                font-size: 1.5em;
            }}
            .weather-panel .forecast-columns {{
                display: flex;
                overflow-x: auto;
            }}
            .weather-panel .forecast-column {{
                flex: 0 0 200px;
                margin-right: 10px;
                border-radius: 10px;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.1);
            }}
            .weather-panel .forecast-column .date {{
                font-weight: bold;
            }}
            .weather-panel .forecast-column .forecast-item {{
                    margin-bottom: 10px;
                    font-size: 1em;
            }}
        </style>
    </head>
    <body>
        <div class="main">
            <div class="weather-panel">
                <div class="header">Current Weather Forecast for {city}</div>
                <div class="data">
                <div class="info temperature"><span>Temperature:{temperature}°F</span></div>
                
                <div class="info">Humidity:{humidity}%</div>
            
                <div class="info">{description}</div>
                </div>
            </div>
            <div class="weather-panel">
                <div class="header">Forecasted Weather for the Next 5 Days in {city}</div>
                <div class="forecast-columns">
                    <!-- Forecast columns here -->
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

    forecast_columns_html = ""
    forecast_by_date = {}

    for forecast_item in forecast['list']:
        forecast_date = forecast_item['dt_txt'].split()[0]
        if forecast_date not in forecast_by_date:
            forecast_by_date[forecast_date] = []
        forecast_by_date[forecast_date].append(forecast_item)

    for date, forecast_items in forecast_by_date.items():
        forecast_column_html = f'''
        <div class="forecast-column">
            <div class="date">{date}</div>
        '''

        for forecast_item in forecast_items:
            forecast_time = forecast_item['dt_txt'].split()[1]
            forecast_temperature = forecast_item['main']['temp']
            forecast_humidity = forecast_item['main']['humidity']
            forecast_description = forecast_item['weather'][0]['description']

            forecast_column_html += f'''
            <div class="forecast-item">
                <div class="title">Time</div>
                <div class="info">{forecast_time}</div>
                <div class="title">Temperature</div>
                <div class="info">{forecast_temperature}°F</div>
                <div class="title">Humidity</div>
                <div class="info">{forecast_humidity}%</div>
                <div class="title">Description</div>
                <div class="info">{forecast_description}</div>
            </div>
            '''

        forecast_column_html += '</div>'
        forecast_columns_html += forecast_column_html

    html_content = html_content.replace('<!-- Forecast columns here -->', forecast_columns_html)

    with open('weather_forecast.html', 'w') as file:
        file.write(html_content)

def open_html_in_new_tab():
    webbrowser.open_new_tab('weather_forecast.html')

def search_weather():
    city_name = entry.get()
    current_weather_data, forecast_data = get_weather(city_name)

    if current_weather_data and forecast_data:
        generate_html(current_weather_data, forecast_data)
        open_html_in_new_tab()

window = tk.Tk()
window.title("Weather Forecast")
window.geometry("300x100")

label = tk.Label(window, text="Enter city name:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Search", command=search_weather)
button.pack()

window.mainloop()
