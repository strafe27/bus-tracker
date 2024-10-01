Here's the modified version of your README:

---

# Malaysian Bus Tracking System

The **Malaysian Bus Tracking System** is designed to track the position of buses in Malaysia using the GTFS Realtime API. The system tracks bus locations for both **Prasarana** and **MyBus** services.

The ETL pipeline is capable of handling up to **800 rows of data every 30 seconds**, which amounts to **90,000 rows of data every hour** and over **2,000,000 rows daily**.

The system is divided into several components:
- **API Ingestion**
- **Containerization**
- **ETL Scheduling**
- **Database Management**
- **Visualization**

## ETL Workflow
<p align="center">
  <img src="https://github.com/user-attachments/assets/dcb041d3-94f7-45c6-bbb4-20bac165a4ee" alt="ETL Workflow Diagram">
</p>

### API Ingestion
The data is collected from the Malaysian GTFS Realtime API, which provides real-time positions of buses from Prasarana and MyBus.

<p align="center">
  <img src="https://github.com/user-attachments/assets/246e87aa-d820-4736-8e09-1b3f85362fd9" alt="API Ingestion Diagram">
</p>

### Containerization
The entire system is built within Docker containers to ensure portability and seamless deployment on cloud infrastructure. This involves setting up Dockerfiles, docker-compose configurations, and managing dependencies through `requirements.txt`.

### ETL Scheduling
Using **Apache Airflow**, the system ingests data every 30 seconds and stores it in a **PostgreSQL** database.

<p align="center">
  <img src="https://github.com/user-attachments/assets/73c2101e-c9ab-4c4e-b9ac-6cf712da992d" alt="ETL Scheduling Diagram">
</p>

Successful execution of tasks can be seen below:

<p align="center">
  <img src="https://github.com/user-attachments/assets/4a9bae80-9d77-404c-912d-e9c5ac4c855e" alt="Successful ETL Runs">
</p>

### Database Management
The ingested data is stored in a **PostgreSQL** database, allowing for easy querying and data access.

<p align="center">
  <img src="https://github.com/user-attachments/assets/691cc01f-5a97-4d94-8d08-932116a74b30" alt="Database Structure">
</p>

### Visualization
The data can be visualized to track the movement of buses in real-time, providing insights into bus routes and locations.

--- 

This version improves clarity and provides a more structured explanation of each part of the system.
