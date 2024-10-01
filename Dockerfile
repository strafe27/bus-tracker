# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.6.3-python3.9

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Copy requirements.txt to the container
COPY requirements.txt .

USER airflow

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
