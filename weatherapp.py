import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import io

class AestheticWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("450x750")
        self.root.resizable(False, False)
        
        # Aesthetic Color Palette
        self.bg_gradient_top = "#667eea"  # Soft purple
        self.bg_gradient_bottom = "#764ba2"  # Deep purple
        self.card_bg = "#ffffff"  # White cards
        self.text_primary = "#2d3748"  # Dark gray
        self.text_secondary = "#718096"  # Medium gray
        self.accent_color = "#667eea"  # Purple accent
        self.temp_color = "#f56565"  # Warm red for temp
        
        # Create gradient background
        self.create_gradient_background()
        
        # API Key
        self.api_key = "bd5e378503939ddaee76f12ad7a97608"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        
        self.create_widgets()
    
    def create_gradient_background(self):
        # Create a canvas for gradient background
        self.bg_canvas = tk.Canvas(
            self.root,
            width=450,
            height=750,
            highlightthickness=0
        )
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient
        for i in range(750):
            ratio = i / 750
            r1, g1, b1 = int(self.bg_gradient_top[1:3], 16), int(self.bg_gradient_top[3:5], 16), int(self.bg_gradient_top[5:7], 16)
            r2, g2, b2 = int(self.bg_gradient_bottom[1:3], 16), int(self.bg_gradient_bottom[3:5], 16), int(self.bg_gradient_bottom[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.bg_canvas.create_line(0, i, 450, i, fill=color)
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.bg_canvas.create_polygon(points, **kwargs, smooth=True)
    
    def create_widgets(self):
        # Title
        self.bg_canvas.create_text(
            225, 50,
            text="Weather",
            font=("Helvetica Neue", 36, "bold"),
            fill="white"
        )
        
        # Search Card
        self.create_rounded_rectangle(30, 100, 420, 170, radius=20, fill=self.card_bg, outline="")
        
        # City Entry
        self.city_entry = tk.Entry(
            self.root,
            font=("Helvetica Neue", 14),
            bg=self.card_bg,
            fg=self.text_primary,
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            bd=0
        )
        self.bg_canvas.create_window(100, 135, window=self.city_entry, width=180, height=35)
        self.city_entry.insert(0, "Enter city name")
        self.city_entry.bind("<FocusIn>", self.clear_placeholder)
        self.city_entry.bind("<Return>", lambda e: self.get_weather())
        
        # Search Button
        search_btn = tk.Button(
            self.root,
            text="Search",
            font=("Helvetica Neue", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#5568d3",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.get_weather,
            bd=0
        )
        self.bg_canvas.create_window(320, 135, window=search_btn, width=100, height=35)
        
        # Main Weather Card
        self.main_card = self.create_rounded_rectangle(30, 200, 420, 490, radius=25, fill=self.card_bg, outline="")
        
        # City Name
        self.city_text = self.bg_canvas.create_text(
            225, 240,
            text="",
            font=("Helvetica Neue", 28, "bold"),
            fill=self.text_primary
        )
        
        # Date
        self.date_text = self.bg_canvas.create_text(
            225, 275,
            text="",
            font=("Helvetica Neue", 12),
            fill=self.text_secondary
        )
        
        # Weather Icon (emoji)
        self.weather_icon = self.bg_canvas.create_text(
            225, 330,
            text="",
            font=("Apple Color Emoji", 70),
            fill=self.text_primary
        )
        
        # Temperature
        self.temp_text = self.bg_canvas.create_text(
            225, 410,
            text="",
            font=("Helvetica Neue", 56, "bold"),
            fill=self.temp_color
        )
        
        # Description
        self.desc_text = self.bg_canvas.create_text(
            225, 460,
            text="",
            font=("Helvetica Neue", 16, "italic"),
            fill=self.text_secondary
        )
        
        # Details Cards
        # Feels Like Card
        self.create_rounded_rectangle(30, 520, 205, 620, radius=20, fill=self.card_bg, outline="")
        self.bg_canvas.create_text(117, 545, text="Feels Like", font=("Helvetica Neue", 11), fill=self.text_secondary)
        self.feels_text = self.bg_canvas.create_text(117, 580, text="", font=("Helvetica Neue", 26, "bold"), fill=self.text_primary)
        
        # Humidity Card
        self.create_rounded_rectangle(245, 520, 420, 620, radius=20, fill=self.card_bg, outline="")
        self.bg_canvas.create_text(332, 545, text="Humidity", font=("Helvetica Neue", 11), fill=self.text_secondary)
        self.humidity_text = self.bg_canvas.create_text(332, 580, text="", font=("Helvetica Neue", 26, "bold"), fill=self.text_primary)
        
        # Wind Speed Card
        self.create_rounded_rectangle(30, 640, 205, 740, radius=20, fill=self.card_bg, outline="")
        self.bg_canvas.create_text(117, 665, text="Wind Speed", font=("Helvetica Neue", 11), fill=self.text_secondary)
        self.wind_text = self.bg_canvas.create_text(117, 700, text="", font=("Helvetica Neue", 22, "bold"), fill=self.text_primary)
        
        # Pressure Card
        self.create_rounded_rectangle(245, 640, 420, 740, radius=20, fill=self.card_bg, outline="")
        self.bg_canvas.create_text(332, 665, text="Pressure", font=("Helvetica Neue", 11), fill=self.text_secondary)
        self.pressure_text = self.bg_canvas.create_text(332, 700, text="", font=("Helvetica Neue", 22, "bold"), fill=self.text_primary)
        
        # Load default city
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, "Paris")
        self.get_weather()
    
    def clear_placeholder(self, event):
        if self.city_entry.get() == "Enter city name":
            self.city_entry.delete(0, tk.END)
    
    def get_weather_emoji(self, description, icon_code):
        """Return appropriate emoji based on weather condition"""
        description = description.lower()
        
        # Check if it's night time (icon code ends with 'n')
        is_night = icon_code.endswith('n')
        
        if "clear" in description:
            return "🌙" if is_night else "☀️"
        elif "cloud" in description:
            if "few" in description or "scattered" in description:
                return "🌤️"
            else:
                return "☁️"
        elif "rain" in description or "drizzle" in description:
            if "light" in description:
                return "🌦️"
            else:
                return "🌧️"
        elif "thunder" in description or "storm" in description:
            return "⛈️"
        elif "snow" in description:
            return "❄️"
        elif "mist" in description or "fog" in description or "haze" in description:
            return "🌫️"
        else:
            return "🌤️"
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        
        if not city or city == "Enter city name":
            messagebox.showerror("Error", "Please enter a city name!")
            return
        
        try:
            # Construct the API URL
            complete_url = f"{self.base_url}appid={self.api_key}&q={city}&units=metric"
            
            # Get the response
            response = requests.get(complete_url)
            data = response.json()
            
            # Check if city was found
            if data["cod"] != 200:
                messagebox.showerror("Error", f"City '{city}' not found!")
                return
            
            # Extract weather data
            main_data = data["main"]
            weather_data = data["weather"][0]
            wind_data = data["wind"]
            
            # Update city name
            self.bg_canvas.itemconfig(self.city_text, text=f"{data['name']}, {data['sys']['country']}")
            
            # Current date and time
            now = datetime.now()
            self.bg_canvas.itemconfig(self.date_text, text=now.strftime("%A, %B %d"))
            
            # Weather emoji
            emoji = self.get_weather_emoji(weather_data["description"], weather_data["icon"])
            self.bg_canvas.itemconfig(self.weather_icon, text=emoji)
            
            # Temperature
            temp = round(main_data["temp"])
            self.bg_canvas.itemconfig(self.temp_text, text=f"{temp}°")
            
            # Description
            description = weather_data["description"].title()
            self.bg_canvas.itemconfig(self.desc_text, text=description)
            
            # Feels like
            feels_like = round(main_data["feels_like"])
            self.bg_canvas.itemconfig(self.feels_text, text=f"{feels_like}°C")
            
            # Humidity
            humidity = main_data["humidity"]
            self.bg_canvas.itemconfig(self.humidity_text, text=f"{humidity}%")
            
            # Wind speed
            wind_speed = round(wind_data["speed"] * 3.6, 1)
            self.bg_canvas.itemconfig(self.wind_text, text=f"{wind_speed} km/h")
            
            # Pressure
            pressure = main_data["pressure"]
            self.bg_canvas.itemconfig(self.pressure_text, text=f"{pressure} hPa")
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "No internet connection!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AestheticWeatherApp(root)
    root.mainloop()