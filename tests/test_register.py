import requests
import re

# Server URL
server_url = "http://localhost:5000"

# Start a session to maintain cookies
session = requests.Session()

# First, get the register page to get the CSRF token
register_page = session.get(f"{server_url}/register")
print(f"Register page status code: {register_page.status_code}")

# Extract CSRF token from the register page
csrf_token_match = re.search(r'name="csrf_token" value="([^"]+)"', register_page.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found register CSRF token: {csrf_token}")
else:
    print("Could not find register CSRF token")
    exit(1)

# Register a new user
register_data = {
    "username": "testuser123",
    "password": "password123",
    "confirm_password": "password123",
    "csrf_token": csrf_token
}

# Register
register_response = session.post(f"{server_url}/register", data=register_data)
print(f"Register status code: {register_response.status_code}")
print(f"Register response URL: {register_response.url}")

# Check if we were redirected to the login page
if "login" in register_response.url:
    print("Registration successful! Redirected to login page.")
else:
    print("Registration failed. Response content:")
    print(register_response.text[:500] + "..." if len(register_response.text) > 500 else register_response.text)

# Now try to login with the new user
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
    
    # Now try to add a device
    dashboard_response = session.get(f"{server_url}/dashboard")
    csrf_token_match = re.search(r'const csrfToken = "([^"]+)"', dashboard_response.text)
    if csrf_token_match:
        csrf_token = csrf_token_match.group(1)
        print(f"Found dashboard CSRF token: {csrf_token}")
        
        # Add a device
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
    else:
        print("Could not find dashboard CSRF token")
else:
    print("Login failed. Response content:")
    print(login_response.text[:500] + "..." if len(login_response.text) > 500 else login_response.text)
