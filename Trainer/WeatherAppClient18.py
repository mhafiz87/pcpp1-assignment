import socket
import json

def start_client(host='127.0.0.1', port=65432):
    """
    Start the socket client to request weather data.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        city_name = input("Enter city name: ")
        client_socket.sendall(city_name.encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        weather_data = json.loads(data)
        
        if "error" in weather_data:
            print(f"Error: {weather_data['error']}")
        else:
            print(f"Weather in {weather_data['name']}:")
            print(f"Temperature: {weather_data['main']['temp']}°C")
            print(f"Weather: {weather_data['weather'][0]['description']}")

if __name__ == "__main__":
    start_client()
