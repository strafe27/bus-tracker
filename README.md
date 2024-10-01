The Malaysian Bus Tracking System is used to track the position of all buses available from the Malaysian GTFS Realtime API. 

Thge ETL pipeline is designed to handle up to  800 rows of data every 30 second, which is 90,000 rows of data every hour and more than 2,000,000 rows of data daily.

This system is split into several parts which is API ingestion, Dockerization, ETL Scheduling, Databasing and Visualisation.

ETL Workflow

<p align="center">
  <img src="https://github.com/user-attachments/assets/dcb041d3-94f7-45c6-bbb4-20bac165a4ee"
</p>
