# Testing Guide for Find My Laptop Application

This guide explains how to test the Find My Laptop application. It's designed for beginners who want to understand how to verify that the application is working correctly.

## Table of Contents

1. [Introduction to Testing](#introduction-to-testing)
2. [Setting Up Your Testing Environment](#setting-up-your-testing-environment)
3. [Basic Tests](#basic-tests)
   - [Testing User Registration](#testing-user-registration)
   - [Testing User Login](#testing-user-login)
   - [Testing Device Addition](#testing-device-addition)
   - [Testing Geofence Creation](#testing-geofence-creation)
4. [Database Inspection](#database-inspection)
5. [Advanced Testing](#advanced-testing)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)

## Introduction to Testing

Testing is an essential part of software development. It helps ensure that your application works as expected and continues to work correctly as you make changes. The Find My Laptop application includes several test scripts that help verify its functionality.

### Types of Tests in This Project

1. **Functional Tests**: These test the application's features like user registration, login, device addition, and geofence creation.
2. **Database Tests**: These inspect the database to verify that data is being stored correctly.
3. **UI Tests**: These check that the user interface is working properly.

## Setting Up Your Testing Environment

Before you can run the tests, you need to set up your testing environment.

### Prerequisites

1. **Python**: Make sure you have Python 3.6 or higher installed.
2. **Required Packages**: Install the necessary Python packages:

```bash
pip install requests
```

3. **Running Server**: The tests assume that the Find My Laptop server is running on `http://localhost:5000`. Start the server before running tests:

```bash
python track_server.py
```

### Test Files Location

All test files are located in the `tests` directory:

- `test_register.py`: Tests user registration
- `test_login.py`: Tests user login
- `test_add_device.py`: Tests adding a device and a geofence
- `test_geofence.py`: Tests adding a geofence to an existing device
- `check_db.py`: Inspects the database
- `check_dashboard.py`: Saves the dashboard HTML for inspection

## Basic Tests

### Testing User Registration

The `test_register.py` script tests the user registration process. It:

1. Gets the registration page and extracts the CSRF token
2. Submits a registration form with a test username and password
3. Verifies that registration was successful
4. Logs in with the new user
5. Adds a test device

To run this test:

```bash
python tests/test_register.py
```

Expected output:
```
Register page status code: 200
Found register CSRF token: [token value]
Register status code: 302
Register response URL: http://localhost:5000/login
Registration successful! Redirected to login page.
Found login CSRF token: [token value]
Login status code: 302
Login response URL: http://localhost:5000/dashboard
Login successful! Redirected to dashboard.
Found dashboard CSRF token: [token value]
Add device status code: 200
Add device response: {"status": "success", "device_id": 1}
```

**What to look for:**
- The registration should redirect to the login page
- The login should redirect to the dashboard
- The device addition should return a success status

### Testing User Login

The `test_login.py` script tests the user login process. It:

1. Gets the login page and extracts the CSRF token
2. Submits a login form with a test username and password
3. Verifies that login was successful

To run this test:

```bash
python tests/test_login.py
```

Expected output:
```
Login page status code: 200
Found login CSRF token: [token value]
Login status code: 302
Login response URL: http://localhost:5000/dashboard
Login successful! Redirected to dashboard.
```

**What to look for:**
- The login should redirect to the dashboard
- If login fails, check that the username and password match a registered user

### Testing Device Addition

The `test_add_device.py` script tests adding a device and a geofence. It:

1. Logs in with a test user
2. Gets the dashboard page and extracts the CSRF token
3. Adds a test device
4. Gets the device page and extracts the CSRF token
5. Adds a test geofence

To run this test:

```bash
python tests/test_add_device.py
```

Expected output:
```
Login page status code: 200
Found login CSRF token: [token value]
Login status code: 302
Dashboard status code: 200
Found CSRF token: [token value]
Add device status code: 200
Add device response: {"status": "success", "device_id": 1}
Found device ID: 1
Device page status code: 200
Found CSRF token: [token value]
Add geofence status code: 200
Add geofence response: {"status": "success"}
```

**What to look for:**
- The device addition should return a success status
- The geofence addition should return a success status
- If either fails, check the error message in the response

### Testing Geofence Creation

The `test_geofence.py` script focuses specifically on adding a geofence to an existing device. It:

1. Logs in with a test user
2. Gets the dashboard page and extracts a device ID
3. Gets the device page and extracts the CSRF token
4. Adds a test geofence
5. Verifies that the geofence appears on the device page

To run this test:

```bash
python tests/test_geofence.py
```

Expected output:
```
Found login CSRF token: [token value]
Login status code: 302
Login response URL: http://localhost:5000/dashboard
Login successful! Redirected to dashboard.
Found device ID: 1
Found device page CSRF token: [token value]
Add geofence status code: 200
Add geofence response: {"status": "success"}
Geofence was successfully added!
```

**What to look for:**
- The geofence addition should return a success status
- The script should confirm that the geofence appears on the device page
- If it fails, check that the device ID exists and belongs to the test user

## Database Inspection

The `check_db.py` script inspects the database to verify that data is being stored correctly. It:

1. Connects to the SQLite database
2. Lists all tables
3. Shows all users
4. Shows all devices
5. Shows all geofences

To run this test:

```bash
python tests/check_db.py
```

Expected output:
```
Tables in the database:
- users
- devices
- locations
- geofences

Users:
ID: 1, Username: testuser123

Devices:
ID: 1, Name: Test Device, Type: Laptop, User ID: 1

Geofences:
ID: 1, Name: Test Geofence, Device ID: 1, Lat: 40.7128, Lon: -74.006, Radius: 1.0
```

**What to look for:**
- Verify that the users, devices, and geofences you've created appear in the database
- Check that the relationships are correct (e.g., devices belong to the right user)
- Confirm that geofence coordinates and radius are stored correctly

## Advanced Testing

### Checking the Dashboard HTML

The `check_dashboard.py` script saves the dashboard HTML to a file for inspection. This is useful for debugging UI issues. It:

1. Logs in with a test user
2. Gets the dashboard page
3. Saves the HTML to a file

To run this test:

```bash
python tests/check_dashboard.py
```

Expected output:
```
Login page status code: 200
Found login CSRF token: [token value]
Login status code: 302
Dashboard status code: 200
Dashboard HTML saved to dashboard.html
```

**What to look for:**
- Open the saved HTML file to inspect the dashboard structure
- Check for any JavaScript errors or missing elements
- Verify that devices are listed correctly

### Creating Custom Tests

You can create your own test scripts based on the examples provided. Here's a template for a basic test:

```python
import requests
import re

# Server URL
server_url = "http://localhost:5000"

# Start a session to maintain cookies
session = requests.Session()

# Get a page and extract CSRF token
response = session.get(f"{server_url}/some-page")
csrf_token_match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
if csrf_token_match:
    csrf_token = csrf_token_match.group(1)
    print(f"Found CSRF token: {csrf_token}")
else:
    print("Could not find CSRF token")
    exit(1)

# Make a POST request
data = {
    "some_field": "some_value",
    "csrf_token": csrf_token
}
response = session.post(f"{server_url}/some-endpoint", json=data, headers={"Content-Type": "application/json"})
print(f"Response status code: {response.status_code}")
print(f"Response: {response.text}")
```

## Troubleshooting Common Issues

### CSRF Token Issues

If you see "Could not find CSRF token" errors:

1. The regular expression might not match the token format in the HTML
2. The page might not include a CSRF token
3. The server might be returning an error page instead of the expected page

Solution: Print the page content to inspect it:
```python
print(response.text)
```

### Authentication Issues

If login or registration fails:

1. Check that the username and password are correct
2. Verify that the CSRF token is being included correctly
3. Look for any error messages in the response

Solution: Print the response URL and content:
```python
print(f"Response URL: {response.url}")
print(response.text[:500])  # Print first 500 characters
```

### API Request Issues

If API requests fail:

1. Ensure you're using the correct Content-Type header
2. Verify that the request body is properly formatted
3. Check that all required fields are included

Solution: Print the request details:
```python
print(f"Request URL: {server_url}/api/endpoint")
print(f"Request data: {data}")
```

### Database Connection Issues

If database inspection fails:

1. Make sure the database file exists
2. Check that the path to the database is correct
3. Verify that the tables exist

Solution: Add error handling:
```python
try:
    conn = sqlite3.connect('device_tracker.db')
    # ... database operations ...
except sqlite3.Error as e:
    print(f"Database error: {e}")
```

## Conclusion

Testing is an ongoing process. As you add features to your application, create new tests to verify that they work correctly. The test scripts provided are a starting point - feel free to modify them or create new ones to suit your needs.

Remember that tests should be:
- Repeatable: They should produce the same results when run multiple times
- Independent: One test should not depend on another test
- Focused: Each test should verify a specific piece of functionality
- Clear: It should be obvious what each test is checking

Happy testing!
