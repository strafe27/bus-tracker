from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
import pytz
from datetime import datetime
from requests import get

# Function to extract data from GTFS Realtime feed
def extract_data(url):
    feed = gtfs_realtime_pb2.FeedMessage()  # GTFS feed message object
    response = get(url)  # Fetch the data from the URL
    feed.ParseFromString(response.content)  # Parse the response content
    
    # Extract only the required fields: tripID, routeID, latitude, longitude, bearing, speed, vehicleID
    vehicle_positions = []
    for entity in feed.entity:
        vehicle_dict = MessageToDict(entity.vehicle)
        
        trip_id = vehicle_dict.get('trip', {}).get('tripId', None)
        route_id = vehicle_dict.get('trip', {}).get('routeId', None)
        latitude = vehicle_dict.get('position', {}).get('latitude', None)
        longitude = vehicle_dict.get('position', {}).get('longitude', None)
        bearing = vehicle_dict.get('position', {}).get('bearing', None)
        speed = vehicle_dict.get('position', {}).get('speed', None)
        vehicle_id = vehicle_dict.get('vehicle', {}).get('id', None)
        
        vehicle_positions.append({
            'trip_id': trip_id,
            'route_id': route_id,
            'latitude': latitude,
            'longitude': longitude,
            'bearing': bearing,
            'speed': speed,
            'vehicle_id': vehicle_id
        })
    
    return vehicle_positions

# Function to process the data into a DataFrame and append it
def create_dataframe(vehicle_positions, agency_name, df=None):
    # Get current timestamp in Malaysia (Asia/Kuala_Lumpur) and format it to include only up to seconds
    malaysia_timezone = pytz.timezone('Asia/Kuala_Lumpur')
    current_time_malaysia = datetime.now(malaysia_timezone).strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert list of dicts to DataFrame
    new_df = pd.DataFrame(vehicle_positions)
    
    # Add current timestamp as the first column
    new_df.insert(0, 'current_timestamp', current_time_malaysia)
    
    # Add agency name as the second column
    new_df.insert(1, 'agency', agency_name)
    
    # Check if the new DataFrame is empty before concatenating
    if new_df.empty:
        print(f"No data found for {agency_name}. Skipping concatenation.")
        return df  # Return original DataFrame if no new data
    
    # If df is None, initialize it with new_df; otherwise, concatenate the data
    if df is not None and not df.empty:
        df = pd.concat([df, new_df], ignore_index=True)  # Append if DataFrame exists
    else:
        df = new_df  # Initialize DataFrame if it's the first data
    
    return df

# List of GTFS-R URLs and their corresponding agencies
url_agency_map = [
    ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl', 'Rapid Bus KL'),
    ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder', 'Rapid Bus MRT Feeder'),
    ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kuantan', 'Rapid Bus Kuantan'),
    ('https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-penang', 'Rapid Bus Penang'),
    ('https://api.data.gov.my/gtfs-realtime/vehicle-position/mybas-johor', 'Mybas Johor')
]

# Initialize an empty DataFrame to store vehicle positions
df = None

# Loop through each URL and agency to fetch and append vehicle data
for url, agency_name in url_agency_map:
    vehicle_positions = extract_data(url)
    df = create_dataframe(vehicle_positions, agency_name, df)

print(f"There are {len(df)} rows")
print(df.head())