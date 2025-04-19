import requests
import json
import re

# Server URL
server_url = "http://localhost:5000"

# Start a session to maintain cookies
session = requests.Session()

# First, get the login page to get the CSRF token
login_page = session.get(f"{server_url}/login")
print(f"Login page status code: {login_page.status_code}")

# Extract CSRF token from the login page
csrf_token_match = re.search(r'name="csrf_token" value="([^"]+)"', login_page.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found login CSRF token: {csrf_token}")
else:
    print("Could not find login CSRF token")
    exit(1)

# Login to get a session
login_data = {
    "username": "test",
    "password": "password123",
    "csrf_token": csrf_token
}

# Login
login_response = session.post(f"{server_url}/login", data=login_data)
print(f"Login status code: {login_response.status_code}")

# Get CSRF token from the dashboard page
dashboard_response = session.get(f"{server_url}/dashboard")
print(f"Dashboard status code: {dashboard_response.status_code}")

# Extract CSRF token from the HTML (this is a simple approach and might be fragile)
import re
csrf_token_match = re.search(r'const csrfToken = "([^"]+)"', dashboard_response.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found CSRF token: {csrf_token}")
else:
    print("Could not find CSRF token")
    exit(1)

# Try to add a device
device_data = {
    "device_name": "Test Device",
    "device_type": "Laptop",
    "csrf_token": csrf_token
}

add_device_response = session.post(
    f"{server_url}/api/register_device",
    json=device_data,
    headers={"Content-Type": "application/json"}
)

print(f"Add device status code: {add_device_response.status_code}")
print(f"Add device response: {add_device_response.text}")

# Try to add a geofence
# First, get a device ID
device_id = None
dashboard_response = session.get(f"{server_url}/dashboard")
device_id_match = re.search(r'href="/device/(\d+)"', dashboard_response.text)
if device_id_match:
    device_id = device_id_match.group(1)
    print(f"Found device ID: {device_id}")
else:
    print("Could not find device ID")
    exit(1)

# Get CSRF token from the device page
device_response = session.get(f"{server_url}/device/{device_id}")
print(f"Device page status code: {device_response.status_code}")

csrf_token_match = re.search(r'const csrfToken = "([^"]+)"', device_response.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found CSRF token: {csrf_token}")
else:
    print("Could not find CSRF token")
    exit(1)

# Add a geofence
geofence_data = {
    "device_id": device_id,
    "name": "Test Geofence",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "radius": 1.0,
    "csrf_token": csrf_token
}

add_geofence_response = session.post(
    f"{server_url}/api/add_geofence",
    json=geofence_data,
    headers={"Content-Type": "application/json"}
)

print(f"Add geofence status code: {add_geofence_response.status_code}")
print(f"Add geofence response: {add_geofence_response.text}")
