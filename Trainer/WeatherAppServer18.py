import socket
import requests
import json

API_KEY = 'c052494dbe0284f55754701467046c59'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_data(city_name):
    """
    Fetch weather data for a city using OpenWeatherMap API.
    """
    params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "City not found or API request failed."}

def start_server(host='127.0.0.1', port=65432):
    """
    Start the socket server to handle weather data requests.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received request for city: {data}")
                weather_data = fetch_weather_data(data)
                conn.sendall(json.dumps(weather_data).encode('utf-8'))

if __name__ == "__main__":
    start_server()
