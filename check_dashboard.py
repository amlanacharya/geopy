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

# Get dashboard page
dashboard_response = session.get(f"{server_url}/dashboard")
print(f"Dashboard status code: {dashboard_response.status_code}")

# Save the dashboard HTML to a file for inspection
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_response.text)
print("Dashboard HTML saved to dashboard.html")
