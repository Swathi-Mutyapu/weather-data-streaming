# 🌦️ Weather Data Streaming Pipeline

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Kafka](https://img.shields.io/badge/kafka-streaming-blue)](https://kafka.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-db-blue)](https://www.postgresql.org/)
[![Made with Python](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)

---

## 📖 About the Project

This project demonstrates a complete **real-time data streaming pipeline** using:
- **Apache Kafka** for event streaming
- **Python** Kafka Producer and Consumer
- **PostgreSQL** as the data sink
- **Docker Compose** to orchestrate the entire system

Weather data is generated (mock or live) and published into a Kafka topic by a **Producer**.  
A **Consumer** listens to the topic, processes the data, and stores it into a **PostgreSQL** database.

➡️ It's a simple but powerful example to understand the flow of data streaming end-to-end!

---

## 🛠️ Technologies Used
- **Apache Kafka** for real-time event streaming
- **Python 3.8+** for Producer and Consumer scripts
- **PostgreSQL 14** for persistent storage
- **Docker & Docker Compose** for local orchestration

---

## 📂 Project Structure
```bash
data-streaming-pipeline/
├── docker-compose.yml
├── kafka-producer/
│   ├── Dockerfile
│   └── python-producer.py
│   └── requirements.txt
├── kafka-consumer/
│   ├── Dockerfile
│   └── python-consumer.py
│   └── requirements.txt
├── .env
├── postgres/
│   └── (uses official postgres image, no custom code needed)
└── README.md
```

---

## 🚀 How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/<your-github-username>/data-streaming-pipeline.git
cd weather-data-streaming
```

2. **Start all services with Docker Compose**
```bash
docker-compose up --build
```

3. **Access PostgreSQL Database**
You can connect using a tool like DBeaver:
- Host: `localhost`
- Port: `5438`
- Username: `postgres`
- Password: `postgres`
- Database: `postgres`

4. **Query the Weather Data**
```sql
SELECT * FROM weather_data LIMIT 5;
```

---

## 📈 What Happens Behind the Scenes?

- The **Producer** fetches (or generates) weather data and pushes JSON messages into the Kafka topic `weather`.
- The **Kafka Consumer** listens to the topic, deserializes the message, and inserts the weather readings into a table called `weather_data` in PostgreSQL.
- **Docker Compose** ensures services (Kafka, Zookeeper, Producer, Consumer, and Postgres) start correctly with dependencies.

---

## 📝 Producer Details

The Producer is responsible for:
- Connecting to the Kafka broker
- Formatting weather data into JSON messages
- Publishing these messages to a Kafka topic (`weather`) at regular intervals

This simulates real-world sensor data generation, similar to IoT devices or weather stations.

---

## 📝 Consumer Details

The Consumer is responsible for:
- Connecting to the Kafka broker
- Listening to the `weather` topic
- Deserializing incoming JSON messages
- Inserting valid records into the PostgreSQL table `weather_data`
- **Ensuring reliability** by committing Kafka offsets after successful processing

This ensures that no data is lost and that every weather event is stored exactly once!

---

## 📋 Importance of `docker-compose.yml`

The `docker-compose.yml` file acts like the **heart** of the project:
- It defines services (Kafka, Zookeeper, Producer, Consumer, PostgreSQL)
- It handles service **dependencies** (e.g., Kafka waits for Zookeeper)
- It makes deployment **one-command simple** (no need to start each service manually)
- It allows you to run a full microservice-style architecture **locally** with zero manual setup

Without it, setting up Kafka + Zookeeper + Producer + Consumer + Postgres would be painful!

---

## 📬 Contact

Feel free to connect or reach out for collaborations:

- [LinkedIn](https://www.linkedin.com/in/swathi-mutyapu/)
- [Personal Website / Portfolio](https://swathimutyapu.com)
