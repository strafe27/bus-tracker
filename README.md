The Malaysian Bus Tracking System is used to track the position of all buses available from the Malaysian GTFS Realtime API.

Using the system, it is possible to track the locations of busses from Prasana and MyBus

Thge ETL pipeline is designed to handle up to  800 rows of data every 30 second, which is 90,000 rows of data every hour and more than 2,000,000 rows of data daily.

This system is split into several parts which is API ingestion, Contenarization, ETL Scheduling, Databasing and Visualisation.

ETL Workflow

<p align="center">
  <img src="https://github.com/user-attachments/assets/dcb041d3-94f7-45c6-bbb4-20bac165a4ee"
</p>

API Ingestion

<p align="center">
  <img src="https://github.com/user-attachments/assets/246e87aa-d820-4736-8e09-1b3f85362fd9"
</p>

Contenarization

The program is built in a container so that it could be deployed onto a cloud computer. This includes setting up Dockerfile, docker-compose, requirements and others

ETL Scheduling

Using Apache Airflow, every 30 second, data is ingested, then load into the PostgreSQL database

<p align="center">
  <img src="https://github.com/user-attachments/assets/73c2101e-c9ab-4c4e-b9ac-6cf712da992d"
</p>

The suffessful runs can be seen below.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4a9bae80-9d77-404c-912d-e9c5ac4c855e"
</p>

Databasing

The data can then be accessed throught the PostgreSQL database

<p align="center">
  <img src="https://github.com/user-attachments/assets/691cc01f-5a97-4d94-8d08-932116a74b30"
</p>

Visualization

The data can then be visualised to track the movements of every bus
