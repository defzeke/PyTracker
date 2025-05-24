import customtkinter as ctk
import requests
import datetime as dt



class Weather(ctk.CTkFrame):
    def __init__(self, user=None):
        root = ctk.CTk()
        root.geometry("800x600")
        

        self.coord_base_url = "http://api.openweathermap.org/geo/1.0/direct?q="
        self.fc_weather_base_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.curr_weather_base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.api_key = open("attendance/modules/weather_key.txt", "r").read()
        self.city = "Manila"
        self.user = user

        self.get_weather()
        for item in self.forecast: print(item)
        print(self.curr_weather)
        

    def get_weather(self):
        try:
            status_code = self.get_coord()
            status_code, self.forecast = self.get_weather_forecast()
            status_code, self.curr_weather = self.get_curr_weather()
        except requests.exceptions.HTTPError as HTTPError:
            match status_code:
                case 400:
                    print("Bad Request")
                case 401:
                    print("Invalid API key")
                case 403:
                    print("Access denied")
                case 404:
                    print("City Not Found")
                case 429:
                    print("API key response limit passed")
                case 500:
                    print("Internal Server Error\nPlease try again later")
                case 502:
                    print("Bad Gateway\nInvalid response from the server")
                case 503:
                    print("Server Unavailable\nServer is down")
                case 504:
                    print("Gateway Timout\nNo response from the server")
                case _:
                    print(f"HTTP error occured\n{HTTPError}")

        except requests.exceptions.ConnectionError:
            print("Check your connection")
        except requests.exceptions.Timeout:
            print("Timeout error\nrequest has timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects\nCheck URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error\n {req_error}")


    def get_coord(self):
        coord_url = f"{self.coord_base_url}{self.city}&limit=5&appid={self.api_key}"

        response = requests.get(coord_url)
        response.raise_for_status()
        data = response.json()


        for item in range(len(data)):
            if data[item]['country'] == 'PH':
                self.lat = data[item]['lat']
                self.lon = data[item]['lon']

        """
        pwedeng wala na tong function and constant na lat and lon ng Manila ilagay, 
        but putting it here if y'all want for the user to search for the city. 
        Ang problem nmn w the user being able to search is may limit yung usage ng api na 60 per min na calls lng
        """

        return response.status_code

    
    def get_weather_forecast(self):
        weather_url = f"{self.fc_weather_base_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}"

        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json() #5 day 3 hours forecast

        forecast = []
        curr_hr = dt.datetime.now().strftime("%H")

        #get specific hr weather from data
        for item in range(16):
            data_dt = data['list'][item]['dt_txt'].split()
            data_t = data_dt[1].split(":") #get time from data

            if data_t[0] > curr_hr: #get future forecast per 3 hour
                forecast.append([data_dt, 
                                 data['list'][item]['weather'][0]['description'],
                                 round(data['list'][item]['main']['temp'] - 273.15)])
            
            if len(forecast) == 7: break


        return response.status_code, forecast
    

    def get_curr_weather(self):
        weather_url = f"{self.curr_weather_base_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}"

        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()

        #get current weather
        curr_temp = round(int(data['main']['temp']) - 273.15)
        curr_w_desc = data['weather'][0]['description']

        curr_weather = [curr_temp, curr_w_desc]

        return response.status_code, curr_weather


if __name__ == "__main__":
    app = Weather()