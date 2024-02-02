import requests
import tkinter as tk
from PIL import Image, ImageTk


API_KEY = '1559383248d001db83f3297a36fc64d0'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

def get_weather():
    city = city_entry.get()
    params = {'q': city, 'appid': API_KEY}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        weather_data = response.json()

        if 'list' in weather_data and len(weather_data['list']) > 0:
            first_forecast = weather_data['list'][0]
            weather_info = f"First forecast entry for {city}:\n"
            weather_info += f"Timestamp: {first_forecast['dt']}\n"
            weather_info += f"Weather: {first_forecast['weather'][0]['description']}\n"
            
            main_info = first_forecast.get('main', {})
            temperature_celsius = main_info.get('temp', 'N/A')
            temperature_fahrenheit = round((temperature_celsius - 273.15) * 9/5 + 32, 2)
            humidity = main_info.get('humidity', 'N/A')

            weather_info += f"Temperature: {temperature_fahrenheit}°F\n"
            weather_info += f"Humidity: {humidity}%"
            
            weather_label.config(text=weather_info)

            
        else:
            weather_label.config(text=f'Weather information not found for {city}.')

    except requests.exceptions.HTTPError as errh:
        weather_label.config(text=f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        weather_label.config(text=f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        weather_label.config(text=f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        weather_label.config(text=f"Error: {err}")
    except requests.exceptions.JSONDecodeError:
        weather_label.config(text='Failed to decode JSON. The response may not be in the expected format.')

def on_enter_key(event):
    get_weather()

def generate_daily_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()

        quote_data = response.json()
        quote_text = quote_data.get('content', 'Unknown Quote')
        quote_author = quote_data.get('author', 'Unknown Author')

        return f"Daily Quote:\n'{quote_text}' - {quote_author}"

    except requests.exceptions.RequestException:
        return "Failed to fetch daily quote."

def display_weather_icon(icon_path):
    # Load and display weather icon in the window
    image = Image.open(icon_path)
    image = image.resize((100, 100), Image.ANTIALIAS)
    icon = ImageTk.PhotoImage(image)
    weather_icon_label.config(image=icon)
    weather_icon_label.image = icon

# Create the main application window
app = tk.Tk()
app.title("Weather App by Anthony Fondo")  

# Get screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set window size and position
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
app.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

# Set background color
app.configure(bg='#87CEEB')  # Sky Blue

# Create and place widgets in the window
tk.Label(app, text="Enter city name:", font=("Helvetica", 16), bg='#87CEEB').pack(pady=10)
city_entry = tk.Entry(app, font=("Helvetica", 16))
city_entry.pack(pady=10)

get_weather_button = tk.Button(app, text="Get Weather", command=get_weather, font=("Helvetica", 16), bg='#4682B4', fg='white')
get_weather_button.pack(pady=20)

weather_label = tk.Label(app, text="", font=("Helvetica", 16), wraplength=window_width - 20, justify='left', bg='#87CEEB')
weather_label.pack(pady=10)

# Display weather icon
weather_icon_label = tk.Label(app, bg='#87CEEB')
weather_icon_label.pack(pady=20)

# Bind Enter key to trigger get_weather
city_entry.bind('<Return>', on_enter_key)

# Generate and display daily quote
daily_quote_label = tk.Label(app, text=generate_daily_quote(), font=("Helvetica", 14), wraplength=window_width - 20, justify='center', bg='#87CEEB')
daily_quote_label.pack(pady=10)

# Display information about me
creator_info_label = tk.Label(app, text="Made by Anthony Fondo", font=("Helvetica", 12), bg='#87CEEB')
creator_info_label.pack(pady=5)

# Start the Tkinter event loop
app.mainloop()
