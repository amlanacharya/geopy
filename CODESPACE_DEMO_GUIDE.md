# GitHub Codespaces Demo Guide: Find My Laptop

This guide explains how to demonstrate the Find My Laptop application using two GitHub Codespaces from the same repository, with one acting as the server and the other as the client.

## Overview

In this demonstration, we'll:
1. Create two separate GitHub Codespaces from different branches
2. Configure one Codespace to run the server component
3. Configure the other Codespace to run the client component
4. Demonstrate the full functionality of the application

## Prerequisites

- GitHub account with access to the repository
- Basic familiarity with GitHub Codespaces
- Basic understanding of Git branching

## Step 1: Prepare the Repository Branches

First, we need to ensure we have two branches in our repository:

1. **Main Branch (`main`)**: This will be used for the server component
2. **Client Branch (`client`)**: This will be used for the client component

If the client branch doesn't exist yet, create it:

```bash
# Clone the repository locally
git clone https://github.com/yourusername/find-my-laptop.git
cd find-my-laptop

# Create and push the client branch
git checkout -b client
git push -u origin client
```

## Step 2: Launch the Server Codespace

1. Go to your GitHub repository in a web browser
2. Click the green "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"
5. Wait for the Codespace to initialize

This Codespace will run the server component of your application.

## Step 3: Configure and Start the Server

In the server Codespace:

1. Open a terminal in the Codespace
2. Install required dependencies:

```bash
pip install flask requests
```

3. Start the server with port forwarding:

```bash
python track_server.py
```

4. The server should start and display something like:
```
* Serving Flask app 'track_server'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

5. Make note of the Codespace URL. In GitHub Codespaces, the server will be accessible at a URL like:
```
https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev
```

This URL is automatically generated when the Flask application starts on port 5000.

## Step 4: Launch the Client Codespace

1. Open a new browser tab
2. Go to your GitHub repository
3. Click the green "Code" button
4. Select the "Codespaces" tab
5. Click "Create codespace on client"
6. Wait for the Codespace to initialize

This Codespace will run the client component of your application.

## Step 5: Configure and Start the Client

In the client Codespace:

1. Open a terminal in the Codespace
2. Install required dependencies:

```bash
pip install requests
```

3. Create a configuration file for the client:

```bash
mkdir -p ~/.laptop_tracker
cat > ~/.laptop_tracker/config.ini << EOF
[SERVER]
url = https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev

[USER]
username = demo_user
password = demo_password
EOF
```

Replace the URL with the actual URL from your server Codespace.

4. Start the client:

```bash
python track_client.py
```

## Step 6: Demonstrate the Application

Now you can demonstrate the full functionality of the application:

### Server-Side Demonstration:

1. **User Registration**:
   - Open the server URL in a browser
   - Click "Register" and create a new account with the same credentials used in the client config (demo_user/demo_password)

2. **Web Interface**:
   - Log in with the credentials
   - Explore the dashboard
   - View registered devices (the client should have registered automatically)

3. **Geofence Creation**:
   - Click on a device to view details
   - Add a geofence with coordinates near the reported location
   - Demonstrate how geofence violations are detected

### Client-Side Demonstration:

1. **Client Registration**:
   - Show the client terminal output
   - Point out the successful registration and device ID assignment

2. **Location Updates**:
   - Explain how the client is sending periodic location updates
   - Show the logs indicating successful updates

3. **Configuration Management**:
   - Show how the client reads from the config file
   - Demonstrate command-line overrides:
   ```bash
   python track_client.py --interval 30
   ```

## Step 7: Demonstrate Cross-Codespace Communication

To clearly show the client-server communication:

1. In the server Codespace, tail the logs:
```bash
# If you're using Flask's built-in server, you'll see logs in the terminal
# Otherwise, you can check the application logs
```

2. In the client Codespace, trigger a manual location update:
```bash
# Restart the client with verbose logging
python track_client.py --verbose
```

3. Show how the location update from the client appears in the server logs

4. Refresh the device details page in the browser to show the updated location

## Step 8: Demonstrate Geofence Functionality

1. In the server Codespace browser, create a geofence with coordinates that are outside the current location

2. Wait for the client to send the next location update

3. Show the geofence violation alert in the server interface

## Troubleshooting Common Issues

### CORS Issues

If you encounter CORS (Cross-Origin Resource Sharing) issues:

1. Modify the server code to allow requests from the Codespace domains:

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*.preview.app.github.dev"])
```

2. Install the Flask-CORS package:

```bash
pip install flask-cors
```

### Network Connectivity

If the client cannot connect to the server:

1. Verify the server URL in the client configuration
2. Ensure the server is running and accessible
3. Check if the port is correctly forwarded in the Codespaces settings

### Authentication Issues

If the client fails to authenticate:

1. Verify the username and password in the client configuration
2. Ensure the user is registered on the server
3. Check the server logs for authentication errors

## Conclusion

This demonstration showcases:

1. The distributed nature of the Find My Laptop application
2. The client-server architecture
3. Real-time location tracking and geofencing
4. The web interface for device management
5. The ability to run both components in separate environments

By using GitHub Codespaces, you can easily demonstrate the application without needing to set up local development environments or deploy to production servers.

## Advanced: Simulating Different Locations

To make the demo more interesting, you can simulate different locations in the client:

1. Modify the client code to use fixed coordinates instead of IP-based geolocation:

```python
# Add this function to the client
def get_mock_location():
    # New York coordinates
    return {
        "ip": "192.168.1.1",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "city": "New York",
        "region": "New York",
        "country": "United States"
    }

# Use this function instead of the real geolocation
```

2. Create a sequence of locations to simulate movement:

```python
# Add this to the client
def get_mock_location_sequence():
    locations = [
        {"latitude": 40.7128, "longitude": -74.0060, "city": "New York"},
        {"latitude": 34.0522, "longitude": -118.2437, "city": "Los Angeles"},
        {"latitude": 41.8781, "longitude": -87.6298, "city": "Chicago"},
        {"latitude": 29.7604, "longitude": -95.3698, "city": "Houston"},
        {"latitude": 39.9526, "longitude": -75.1652, "city": "Philadelphia"}
    ]
    
    # Return a different location each time
    import time
    index = int(time.time() / 60) % len(locations)
    location = locations[index]
    location["ip"] = "192.168.1.1"
    location["region"] = "Demo Region"
    location["country"] = "United States"
    return location
```

This will create a more dynamic demonstration of the tracking and geofencing capabilities.
