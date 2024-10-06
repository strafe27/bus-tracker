# Malaysian Bus Tracking System

The **Malaysian Bus Tracking System** is designed to monitor and track bus positions across Malaysia using the **GTFS Realtime API**. The system specifically tracks the near real-time locations of buses operated by **Prasarana** and **MyBus** services.

This includes core services such as
- **Rapid KL**
- **Rapid Penang**
- **Rapid Pahang**
- **Rapid MRT Feeders**
- **Mybas Johor**
  
## Key Features
This ETL pipeline is capable of processing **up to 800 rows every 30 seconds**, which translates to **90,000 rows per hour** and over **2 million rows daily**.

This system comprises the following components:
- **API Ingestion**
- **Containerization**
- **ETL Scheduling**
- **Database Management**
- **Visualization**

## Tools Used
- **Apache Airflow**
- **Docker**
- **PostgreSQL**
- **Seaborn**

---

## ETL Workflow
The diagram below shows the full ETL pipeline, outlining the data flow from ingestion to storage and visualization.

<p align="center">
  <img src="https://github.com/user-attachments/assets/dcb041d3-94f7-45c6-bbb4-20bac165a4ee" alt="ETL Workflow Diagram">
</p>

### API Ingestion
The data is ingested from Malaysia's **GTFS Realtime API**, which provides up-to-date information on the positions of buses for both **Prasarana** and **MyBus**.

<p align="center">
  <img src="https://github.com/user-attachments/assets/246e87aa-d820-4736-8e09-1b3f85362fd9" alt="API Ingestion Diagram">
</p>

### Containerization
The system is containerized using **Docker** to ensure portability and ease of deployment, whether it's on local environments or cloud platforms. This involves setting up **Dockerfiles**, **docker-compose**, and managing dependencies through `requirements.txt`.

### ETL Scheduling
Using **Apache Airflow**, the ETL pipeline is scheduled to run every 30 seconds, ensuring that real-time bus data is continuously ingested and stored in the **PostgreSQL** database.

<p align="center">
  <img src="https://github.com/user-attachments/assets/73c2101e-c9ab-4c4e-b9ac-6cf712da992d" alt="ETL Scheduling Diagram">
</p>

You can view the successful task executions below:

<p align="center">
  <img src="https://github.com/user-attachments/assets/4a9bae80-9d77-404c-912d-e9c5ac4c855e" alt="Successful ETL Runs">
</p>

### Database Management
The ingested bus data is automatically stored in a **PostgreSQL** database. This allows users to easily query the data for analysis or further processing.

<p align="center">
  <img src="https://github.com/user-attachments/assets/691cc01f-5a97-4d94-8d08-932116a74b30" alt="Database Structure">
</p>

### Visualization
The system provides real-time visualization of bus movements across Malaysia. This helps in monitoring bus routes, frequency, and overall operations.

The graph below shows the **number of buses per agency** captured in the morning:

<p align="center">
  <img src="https://github.com/user-attachments/assets/a7dde6a0-eddc-45a0-b32b-89d63fd88c26" alt="Average Buses Per Agency">
</p>

It appears that **MyBus** leads, followed by **Rapid Bus KL**. However, mapping the locations of each bus helps explain this difference.

<p align="center">
  <img src="https://github.com/user-attachments/assets/37baad0b-74e2-4536-a332-e351e71d09d5" alt="Bus Map Visualization">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/881b7615-a50b-4481-808a-833262b228bd" alt="Bus Location Map">
</p>

Upon analyzing the mapped bus locations, it becomes clear that **Rapid KL** primarily covers **interstate trips**, whereas **MyBus** serves both **interstate** and **out-of-state routes**. This explains the higher number of buses in the MyBus fleet.
