import json
import psycopg2
from kafka import KafkaConsumer
import os

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather")
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        feels_like FLOAT,
        humidity INTEGER,
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    data = message.value
    print(f"Received message: {data}")  # Print the raw message

    try:
        city = data.get("city")
        temperature = data.get("temperature")  # Use .get() to avoid missing key errors
        feels_like = data.get("feels_like")
        humidity = data.get("humidity")

        # Check if the values exist before trying to insert
        if city and temperature and feels_like and humidity:
            print(f"Inserting into DB: {city}, {temperature}°C, {feels_like}°C, {humidity}%")
            cursor.execute(
                "INSERT INTO weather_data (city, temperature, feels_like, humidity) VALUES (%s, %s, %s, %s)",
                (city, temperature, feels_like, humidity)
            )
            conn.commit()
            print(f"Inserted into DB: {city}, {temperature}°C, {feels_like}°C, {humidity}%")
        else:
            print("Missing data:", data)
    except Exception as e:
        print("Error inserting into DB:", e)
