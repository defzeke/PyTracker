import customtkinter as ctk
import requests
import datetime as dt
from PIL import ImageTk, Image


class Weather(ctk.CTkFrame):
    def __init__(self, user="Username"):
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.state("zoomed")
        self.root.resizable(False,False)
        
        self.canvas = ctk.CTkCanvas(self.root, width=800, height=600, bg="#E3E9ED")
        self.canvas.pack(fill="both",expand=True)

        self.coord_base_url = "http://api.openweathermap.org/geo/1.0/direct?q="
        self.fc_weather_base_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.curr_weather_base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.api_key = open("attendance/modules/weather_key.txt", "r").read()
        self.city = "Manila"
        self.user = user
        self.curr_dt = dt.datetime.now()

        self.get_weather()

    def run(self):
        self.root.mainloop()

    def draw(self):
        self.canvas.create_rectangle(50, 50, 750, 550, fill="white")

        #draw greetings
        self.canvas.create_text(65, 60, text=f"Hello {self.user}!", font=("Tai Heritage Pro", 50), fill="black", anchor="nw")
        self.canvas.create_text(70, 125, text=f"Check out the weather!", font=("Tai Heritage Pro", 15), fill="black", anchor="nw")
        
        #draw current weather
        self.canvas.create_text(190, 200, text=f"{self.curr_weather[2]}°C", font=("Tai Heritage Pro", 30), fill="black", anchor="nw")
        self.canvas.create_text(290, 203, text=f"{self.curr_weather[1]}", font=("Tai Heritage Pro", 13), fill="black", anchor="nw")
        self.canvas.create_text(195, 244, text=f"as of {self.curr_weather[0][0]} - {self.curr_weather[0][1]}", font=("Tai Heritage Pro", 12), fill="black", anchor="nw")

        self.canvas.create_line(430, 190, 430, 275)
        self.canvas.create_text(460, 190, text=f"Manila,\nMetro Manila", font=("Tai Heritage Pro", 25), fill="black", anchor="nw")

        curr_w_desc = self.get_weather_desc_png(self.curr_weather[3])
        curr_w = Image.open(f"attendance/public/Weather/{curr_w_desc}").resize((150,150), Image.LANCZOS)
        self.curr_png = ImageTk.PhotoImage(curr_w)
        self.curr_w_img = self.canvas.create_image(55, 155, image=self.curr_png, anchor="nw", tags="currw")

        #draw next 21 hrs forecast
        x = 200
        y = 300
        self.forecast_img = []
        self.forecast_png = []

        for item in range(len(self.forecast)):
            if item == 3: 
                y += 115
                x = 115
        
            self.canvas.create_text(x, y, text=f"{self.forecast[item][2]}°C", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
            self.canvas.create_text(x+65, y, text=f"{self.forecast[item][1]}", font=("Tai Heritage Pro", 9), fill="black", anchor="nw")
            self.canvas.create_text(x+5, y+65, text=f"{self.forecast[item][0][0]}\n  {self.forecast[item][0][1]}", font=("Tai Heritage Pro", 9), fill="black", anchor="nw")
            self.canvas.create_line(x-14, y, x-14, y+100)


            forecast_desc = self.get_weather_desc_png(self.forecast[item][3])
            forecast = Image.open(f"attendance/public/Weather/{forecast_desc}").resize((60,60), Image.LANCZOS)
            self.forecast_png.append(ImageTk.PhotoImage(forecast)) 
            self.forecast_img.append(self.canvas.create_image(x, y+15, image=self.forecast_png[item], anchor="nw", tags="currw"))

            
            x += 150
            

    def get_weather_desc_png(self, id=0):
        if 232 >= id >= 200:
            png = "Thunderstorm.png"
        elif 321 >= id >= 300:
            png = "Drizzle.png"
        elif 531 >= id >= 500:
            png = "Rain.png"
        elif 622 >= id >= 600:
            png = "Snow.png"
        elif 781 >= id >= 700:
            png = "Mist.png"
        elif id == 800:
            png = "Clear.png"
        elif 804 >= id >= 800:
            png = "Clouds.png"
        else: 
            png = None

        return png


    def get_weather(self):
        try:
            self.get_coord()
            self.forecast = self.get_weather_forecast()
            self.curr_weather = self.get_curr_weather()

            self.draw()


            for item in self.forecast: print(item)
            print(self.curr_weather)

        except requests.exceptions.HTTPError as HTTPError:
            match self.response.status_code:
                case 400:
                    self.canvas.create_text(400, 500, text=f"Bad Request,\nError 400", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 401:
                    self.canvas.create_text(400, 500, text=f"Invalid API key,\nError 401", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 403:
                    self.canvas.create_text(400, 500, text=f"Access Denied,\nError 403", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 404:
                    self.canvas.create_text(400, 500, text=f"City not Found,\nError 404", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 429:
                    self.canvas.create_text(400, 500, text=f"API key response limit passed,\nError 429", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 500:
                    self.canvas.create_text(400, 500, text=f"Internal Server Error,\nError 500", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 502:
                    self.canvas.create_text(400, 500, text=f"Bad Gateway,\nError 502", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 503:
                    self.canvas.create_text(400, 500, text=f"Server Unavailable,\nError 503", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case 504:
                    self.canvas.create_text(400, 500, text=f"Gateway Timeout,\nError 504", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
                case _:
                    self.canvas.create_text(400, 500, text=f"HTTP error occured,\n{HTTPError}", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
        except requests.exceptions.ConnectionError:
            self.canvas.create_text(400, 500, text=f"Network Error,\nPlease check your connection", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
        except requests.exceptions.Timeout:
            self.canvas.create_text(400, 500, text=f"Timout Error,\nrequest has timed out", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
        except requests.exceptions.TooManyRedirects:
            self.canvas.create_text(400, 500, text=f"Too many redirects,\nCheck URL", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")
        except requests.exceptions.RequestException as req_error:
            self.canvas.create_text(400, 500, text=f"Request Error,\n{req_error}", font=("Tai Heritage Pro", 20), fill="black", anchor="nw")


    def get_coord(self):
        coord_url = f"{self.coord_base_url}{self.city}&limit=5&appid={self.api_key}"

        self.response = requests.get(coord_url)
        self.response.raise_for_status()
        data = self.response.json()


        for item in range(len(data)):
            if data[item]['country'] == 'PH':
                self.lat = data[item]['lat']
                self.lon = data[item]['lon']


    def get_weather_forecast(self):
        weather_url = f"{self.fc_weather_base_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}"

        self.response = requests.get(weather_url)
        self.response.raise_for_status()
        data = self.response.json() #5 day 3 hours forecast

        forecast = []
        curr_hr = self.curr_dt.strftime("%H")
        curr_d = self.curr_dt.strftime("%d")

        #get specific hr weather from data
        for item in range(16):
            data_dt = data['list'][item]['dt_txt'].split()
            data_t = data_dt[1].split(":") #get time from data
            data_d = data_dt[0].split("-") #get day from data

            if data_t[0] > curr_hr or int(data_d[2]) == int(curr_d)+1: #get future forecast per 3 hour
                forecast.append([data_dt, 
                                 data['list'][item]['weather'][0]['description'].replace(" ", "\n"),
                                 round(data['list'][item]['main']['temp'] - 273.15),
                                 data['list'][item]['weather'][0]['id']])
            
            if len(forecast) == 7: break

        return forecast
    

    def get_curr_weather(self):
        weather_url = f"{self.curr_weather_base_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}"

        self.response = requests.get(weather_url)
        self.response.raise_for_status()
        data = self.response.json()

        #get current weather
        curr_temp = round(int(data['main']['temp']) - 273.15)
        curr_w_desc = data['weather'][0]['description'].replace(" ", "\n")
        curr_w_id = data['weather'][0]['id']
        curr_dt = f"{self.curr_dt.replace(microsecond=0)}".split()

        curr_weather = [curr_dt, curr_w_desc, curr_temp, curr_w_id]

        return curr_weather


if __name__ == "__main__":
    app = Weather()
    app.run()