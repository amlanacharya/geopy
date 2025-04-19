import requests
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
print(f"Login response URL: {login_response.url}")

# Check if we were redirected to the dashboard
if "dashboard" in login_response.url:
    print("Login successful! Redirected to dashboard.")
else:
    print("Login failed. Response content:")
    print(login_response.text[:500] + "..." if len(login_response.text) > 500 else login_response.text)
