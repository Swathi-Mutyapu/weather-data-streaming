# Use a Python base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the producer files to the container
COPY . /app

# Install required dependencies
RUN pip install -r requirements.txt

# Command to run the producer
CMD ["python", "python-producer.py"]
