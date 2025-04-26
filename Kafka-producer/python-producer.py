import json
import time
import requests
from kafka import KafkaProducer
import os
import datetime

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather")
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
PRODUCER_INTERVAL = int(os.getenv("PRODUCER_INTERVAL", 60))

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_weather():
    API_KEY = os.getenv("WEATHER_API_KEY")
    CITY = os.getenv("CITY", "London")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    weather = response.json()

    data = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'city': weather['name'],
        'temperature': weather['main']['temp'],
        'feels_like': weather['main']['feels_like'],
        'humidity': weather['main']['humidity'],
        'description': weather['weather'][0]['description']
    }

    return data

while True:
    try:
        weather_data = fetch_weather()
        producer.send(KAFKA_TOPIC, weather_data)
        print(f"Produced weather data: {weather_data}")
    except Exception as e:
        print(f"Error fetching/sending data: {e}")
    time.sleep(PRODUCER_INTERVAL)
