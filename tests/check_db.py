import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('device_tracker.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table['name']}")
    
# Check users
print("\nUsers:")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"ID: {user['id']}, Username: {user['username']}")

# Check devices
print("\nDevices:")
cursor.execute("SELECT * FROM devices")
devices = cursor.fetchall()
for device in devices:
    print(f"ID: {device['id']}, Name: {device['device_name']}, Type: {device['device_type']}, User ID: {device['user_id']}")

# Check geofences
print("\nGeofences:")
cursor.execute("SELECT * FROM geofences")
geofences = cursor.fetchall()
for geofence in geofences:
    print(f"ID: {geofence['id']}, Name: {geofence['name']}, Device ID: {geofence['device_id']}, Lat: {geofence['latitude']}, Lon: {geofence['longitude']}, Radius: {geofence['radius']}")

# Close the connection
conn.close()
