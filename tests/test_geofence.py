import requests
import re

# Server URL
server_url = "http://localhost:5000"

# Start a session to maintain cookies
session = requests.Session()

# Login with the test user
login_page = session.get(f"{server_url}/login")
csrf_token_match = re.search(r'name="csrf_token" value="([^"]+)"', login_page.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found login CSRF token: {csrf_token}")
else:
    print("Could not find login CSRF token")
    exit(1)

login_data = {
    "username": "testuser123",
    "password": "password123",
    "csrf_token": csrf_token
}

login_response = session.post(f"{server_url}/login", data=login_data)
print(f"Login status code: {login_response.status_code}")
print(f"Login response URL: {login_response.url}")

if "dashboard" in login_response.url:
    print("Login successful! Redirected to dashboard.")
    
    # Get the device ID
    dashboard_response = session.get(f"{server_url}/dashboard")
    device_id_match = re.search(r'href="/device/(\d+)"', dashboard_response.text)
    if device_id_match:
        device_id = device_id_match.group(1)
        print(f"Found device ID: {device_id}")
        
        # Get the device page to get the CSRF token
        device_page = session.get(f"{server_url}/device/{device_id}")
        csrf_token_match = re.search(r'const csrfToken = "([^"]+)"', device_page.text)
        if csrf_token_match:
            csrf_token = csrf_token_match.group(1)
            print(f"Found device page CSRF token: {csrf_token}")
            
            # Add a geofence
            geofence_data = {
                "device_id": int(device_id),
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
            
            # Check if the geofence was added by looking at the device page again
            device_page = session.get(f"{server_url}/device/{device_id}")
            if "Test Geofence" in device_page.text:
                print("Geofence was successfully added!")
            else:
                print("Geofence was not found in the device page.")
        else:
            print("Could not find device page CSRF token")
    else:
        print("Could not find device ID")
else:
    print("Login failed.")
