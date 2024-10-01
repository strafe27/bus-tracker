from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from airflow.providers.postgres.operators.postgres import PostgresOperator
import pandas as pd
import pytz
from datetime import datetime
from requests import get
import logging
from datetime import datetime, timedelta


# Function to extract data from GTFS Realtime feed
def extract_data(**context):
    url_agency_map = [
        ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl', 'Rapid Bus KL'),
        ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder', 'Rapid Bus MRT Feeder'),
        ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kuantan', 'Rapid Bus Kuantan'),
        ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-penang', 'Rapid Bus Penang'),
        ('https://api.data.gov.my/gtfs-realtime/vehicle-position/mybas-johor', 'Mybas Johor')
    ]
    
    vehicle_data = []
    for url, agency_name in url_agency_map:
        feed = gtfs_realtime_pb2.FeedMessage()  # GTFS feed message object
        response = get(url)  # Fetch the data from the URL
        feed.ParseFromString(response.content)  # Parse the response content
        
        for entity in feed.entity:
            vehicle_dict = MessageToDict(entity.vehicle)
            
            trip_id = vehicle_dict.get('trip', {}).get('tripId', None)
            route_id = vehicle_dict.get('trip', {}).get('routeId', None)
            latitude = vehicle_dict.get('position', {}).get('latitude', None)
            longitude = vehicle_dict.get('position', {}).get('longitude', None)
            bearing = vehicle_dict.get('position', {}).get('bearing', None)
            speed = vehicle_dict.get('position', {}).get('speed', None)
            vehicle_id = vehicle_dict.get('vehicle', {}).get('id', None)
            
            vehicle_data.append({
                'trip_id': trip_id,
                'route_id': route_id,
                'latitude': latitude,
                'longitude': longitude,
                'bearing': bearing,
                'speed': speed,
                'vehicle_id': vehicle_id,
                'agency': agency_name
            })
    
    context['ti'].xcom_push(key='vehicle_data', value=vehicle_data)


# Function to process the data into a DataFrame
def create_dataframe(**context):
    vehicle_data = context['ti'].xcom_pull(key='vehicle_data', task_ids='extract_data')
    
    if not vehicle_data:
        logging.warning("No vehicle data received.")
        return

    malaysia_timezone = pytz.timezone('Asia/Kuala_Lumpur')
    current_time_malaysia = datetime.now(malaysia_timezone).strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(vehicle_data)
    
    # Add current timestamp as the first column
    df.insert(0, 'timestamp', current_time_malaysia)
    
    # Push the DataFrame to XCom for the next task
    context['ti'].xcom_push(key='vehicle_df', value=df.to_dict(orient='records'))

def load_data_to_postgres(**context):
    vehicle_df = pd.DataFrame(context['ti'].xcom_pull(key='vehicle_df', task_ids='create_dataframe'))
    
    if vehicle_df.empty:
        logging.warning("No data to insert into PostgreSQL.")
        return

    # Connect to PostgreSQL using PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id='postgres_connection')  # Replace with your connection ID

    # Insert the data into the PostgreSQL table (excluding the 'id' column because it's SERIAL)
    insert_query = """
    INSERT INTO vehicle_positions (timestamp, trip_id, route_id, latitude, longitude, bearing, speed, vehicle_id, agency)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    rows = vehicle_df[['timestamp', 'trip_id', 'route_id', 'latitude', 'longitude', 'bearing', 'speed', 'vehicle_id', 'agency']].values.tolist()

    if rows:
        # Specify the columns to insert (excluding the 'id' column)
        postgres_hook.insert_rows('vehicle_positions', rows, 
                                  target_fields=['timestamp', 'trip_id', 'route_id', 'latitude', 'longitude', 'bearing', 'speed', 'vehicle_id', 'agency'])
        logging.info(f"Inserted {len(rows)} rows into the vehicle_positions table.")
    else:
        logging.warning("No rows to insert.")

# Default DAG arguments
default_args = {
    'start_date': datetime(2024, 9, 30),
    'retries': 1,
}

# Define the DAG
with DAG('gtfs_realtime_to_postgres_v3',
    default_args=default_args,
    description='Extract GTFS Realtime data, process it, and load to PostgreSQL',
    schedule_interval=timedelta(seconds=30),  # Run every 30 seconds
    catchup=False,
) as dag:

    # Task 1: Extract data from GTFS Realtime API
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    # Task 2: Create a DataFrame from the extracted data
    transformation = PythonOperator(
        task_id='create_dataframe',
        python_callable=create_dataframe
    )

    # Task 3: Create the table if it doesn't exist
    create_table_task = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_connection',
        sql="""
        CREATE TABLE IF NOT EXISTS vehicle_positions (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            trip_id TEXT,
            route_id TEXT,
            latitude NUMERIC,
            longitude NUMERIC,
            bearing NUMERIC,
            speed NUMERIC,
            vehicle_id TEXT,
            agency TEXT
        );
        """,
        retries=1,
        execution_timeout=timedelta(minutes=2)
    )

    # Task 4: Load the data into PostgreSQL
    load_to_postgres_task = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data_to_postgres,
        retries=1,
        execution_timeout=timedelta(minutes=3)
    )

    # Task dependencies
    extract_task >> transformation >> create_table_task >> load_to_postgres_task
