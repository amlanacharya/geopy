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

In this step, we'll set up and start the server component in the first Codespace. Follow these detailed instructions:

### 3.1 Open a Terminal

1. At the bottom of your Codespace window, you should see a terminal panel
2. If you don't see it, click on Terminal → New Terminal in the top menu
3. The terminal will open with a command prompt showing something like `@yourusername ➜ /workspaces/find-my-laptop $`

### 3.2 Install Required Dependencies

We need to install the necessary Python packages for the server to run:

1. Type the following command in the terminal and press Enter:

```bash
pip install flask requests
```

2. Wait for the installation to complete. You'll see progress information and finally a message like:
```
Successfully installed flask-2.0.1 requests-2.26.0 ...
```

### 3.3 Start the Server

Now let's start the server application:

1. Type the following command and press Enter:

```bash
python track_server.py
```

2. The server will start up and you should see output similar to:
```
* Serving Flask app 'track_server'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://172.16.5.4:5000
```

### 3.4 Find the Public URL

GitHub Codespaces automatically creates a public URL for your server. Here's how to find it:

1. Look for a notification in the bottom right corner that says "Your application running on port 5000 is available."

2. If you see this notification, click on it and select "Open in Browser" to see the URL

3. If you don't see the notification, follow these steps:
   - Look at the bottom of the Codespace window for a "PORTS" tab
   - Click on this tab to open the Ports panel
   - You should see port 5000 listed with a URL like:
     ```
     https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev
     ```
   - Right-click on this URL and select "Copy Port URL"

4. Keep this URL handy - you'll need it to configure the client

5. You can also click on the URL to open the application in a new browser tab

### 3.5 Verify the Server is Running

1. Open the server URL in a new browser tab

2. You should see the Find My Laptop landing page with options to login or register

3. If you see an error or the page doesn't load, check the terminal for any error messages

### 3.6 Keep the Server Running

Important: Keep this terminal and Codespace open throughout the demo. The server needs to keep running for the client to connect to it.

## Step 4: Launch the Client Codespace

1. Open a new browser tab
2. Go to your GitHub repository
3. Click the green "Code" button
4. Select the "Codespaces" tab
5. Click "Create codespace on client"
6. Wait for the Codespace to initialize

This Codespace will run the client component of your application.

## Step 5: Configure and Start the Client

In the client Codespace, we'll need to set up the client configuration and start the application. Follow these detailed steps:

### 5.1 Open a Terminal

1. Look at the bottom of your Codespace window
2. You should see a tab labeled "Terminal"
3. Click on this tab to open the terminal
4. If you don't see a terminal, you can open one by:
   - Clicking on the menu at the top: Terminal → New Terminal
   - Or using the keyboard shortcut: `` Ctrl+` `` (Control + backtick)

### 5.2 Install Required Dependencies

Type the following command in the terminal and press Enter:

```bash
pip install requests
```

You should see output showing the installation progress. Wait until it completes.

### 5.3 Create the Configuration Directory

The client needs a configuration directory. Create it with this command:

```bash
mkdir -p ~/.laptop_tracker
```

This command creates a hidden directory called `.laptop_tracker` in your home directory.

### 5.4 Create the Configuration File

Now we'll create the configuration file that tells the client how to connect to the server:

1. First, copy the server URL from your server Codespace. It should look like:
   ```
   https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev
   ```

2. Create the configuration file using one of these two methods:

   **Method 1: Using a text editor**

   ```bash
   # Open the file in the built-in editor
   code ~/.laptop_tracker/config.ini
   ```

   This will open a new editor tab. Paste the following content, replacing the URL with your actual server URL:

   ```ini
   [SERVER]
   url = https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev

   [USER]
   username = demo_user
   password = demo_password
   ```

   Save the file by pressing Ctrl+S or using File → Save from the menu.

   **Method 2: Using the terminal**

   ```bash
   cat > ~/.laptop_tracker/config.ini << EOF
   [SERVER]
   url = https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev

   [USER]
   username = demo_user
   password = demo_password
   EOF
   ```

   Make sure to replace the URL with your actual server URL.

### 5.5 Verify the Configuration File

Let's make sure the configuration file was created correctly:

```bash
cat ~/.laptop_tracker/config.ini
```

This should display the contents of the file. Verify that the URL, username, and password are correct.

### 5.6 Start the Client

Now you're ready to start the client application:

```bash
python track_client.py
```

You should see output indicating that the client is starting up and connecting to the server. It will look something like:

```
INFO: Starting Find My Laptop client
INFO: Connecting to server at https://yourusername-find-my-laptop-xxxxxxxxxxxx-5000.preview.app.github.dev
INFO: Registering device with server...
INFO: Device registered successfully with ID: 1
INFO: Starting location update thread
INFO: Sending location update to server...
```

If you see errors, double-check your configuration file and make sure the server is running.

## Step 6: Demonstrate the Application

Now you can demonstrate the full functionality of the application. This section provides a detailed walkthrough for presenting the demo to complete beginners.

### 6.1 Server-Side Demonstration

#### 6.1.1 User Registration

1. **Open the Application**:
   - In your browser, navigate to the server URL you copied earlier
   - You should see the Find My Laptop landing page with a welcome message

2. **Register a New Account**:
   - Click the "Register" button on the landing page
   - Fill in the registration form with these details:
     - Username: `demo_user` (must match what you put in the client config)
     - Password: `demo_password` (must match what you put in the client config)
     - Confirm Password: `demo_password` (type it again)
   - Click the "Register" button to create the account
   - You should be redirected to the login page with a success message

3. **Explain the Process**:
   - Point out that the registration created a new user in the database
   - Mention that passwords are securely hashed, not stored in plain text
   - Explain that this account will be used by both the web interface and the client application

#### 6.1.2 Web Interface Tour

1. **Login to the Dashboard**:
   - On the login page, enter the username and password you just created
   - Click the "Login" button
   - You should be redirected to the dashboard

2. **Explore the Dashboard**:
   - Point out the welcome message with the username
   - If the client is running, you should see a device listed
   - If no devices are shown yet, explain that they'll appear once the client connects
   - Show the "Add Device" button and explain that devices can be added manually or automatically

3. **Wait for Client Registration** (if needed):
   - If the client is running in the other Codespace, wait a moment for it to register
   - Refresh the dashboard page to see the newly registered device
   - Point out the device name, type, and registration date

#### 6.1.3 Geofence Creation and Management

1. **Access Device Details**:
   - Click on the "View Details" link for the device
   - This opens the device details page
   - Point out the current location on the map
   - Show the location history table below the map

2. **Create a Geofence**:
   - Click the "Add Geofence" button
   - A modal window will appear
   - Fill in the geofence details:
     - Name: `Home` or `Office`
     - Latitude: Use a value close to but not exactly the same as the current device location (e.g., if device is at 19.0760, use 19.0750)
     - Longitude: Use a value close to but not exactly the same as the current device location (e.g., if device is at 72.8777, use 72.8767)
     - Radius: `0.5` (0.5 kilometers)
   - Click the "Save Geofence" button

3. **Explain Geofence Visualization**:
   - Point out the circular geofence that appears on the map
   - Explain that the circle represents the boundary
   - Show how the device is currently inside the geofence

### 6.2 Client-Side Demonstration

#### 6.2.1 Client Registration Process

1. **Show the Client Terminal**:
   - Switch to the client Codespace
   - Point to the terminal where the client is running

2. **Explain the Output**:
   - Show the initial connection and registration messages
   - Point out the line that says "Device registered successfully with ID: X"
   - Explain that this ID is used for all future communications

3. **Explain the Registration Process**:
   - The client sends username and password to authenticate
   - It also sends system information (hostname, OS)
   - The server creates a device record and returns an ID
   - This ID is stored by the client for future use

#### 6.2.2 Location Updates

1. **Show Ongoing Updates**:
   - Point out the periodic messages about sending location updates
   - Explain that these happen automatically at regular intervals
   - Show successful update confirmations from the server

2. **Explain the Location Data**:
   - Explain that in a real deployment, the client would use IP-based geolocation
   - For the demo, we're using simulated locations in India
   - Point out the coordinates, city, region, and country information

#### 6.2.3 Configuration Management

1. **Show the Configuration File**:
   - Open a new terminal tab in the client Codespace
   - Run: `cat ~/.laptop_tracker/config.ini`
   - Explain each section and setting

2. **Demonstrate Command-Line Overrides**:
   - Stop the current client by pressing Ctrl+C in its terminal
   - Start it again with different parameters:
   ```bash
   python track_client.py --interval 30 --verbose
   ```
   - Explain that this changes the update frequency to 30 seconds
   - Point out the additional debug information from the --verbose flag

3. **Explain Configuration Priority**:
   - Command-line arguments override config file settings
   - Config file settings override built-in defaults
   - This provides flexibility for different deployment scenarios

## Step 7: Demonstrate Cross-Codespace Communication

This step shows how the two Codespaces communicate with each other, which is a key concept for beginners to understand.

### 7.1 Monitor Server Logs

1. **Switch to the Server Codespace**:
   - Go back to the browser tab with your server Codespace
   - Look at the terminal where the server is running

2. **Explain the Server Logs**:
   - Point out the log entries that appear when requests come in
   - Explain that each line represents a client request to the server
   - Show the HTTP status codes (200 means success)
   - Point out the API endpoints being accessed (e.g., `/api/update_location`)

3. **Keep the Logs Visible**:
   - Position the terminal so it's clearly visible
   - Explain that you'll be watching for new log entries

### 7.2 Trigger a Manual Location Update

1. **Switch to the Client Codespace**:
   - Go to the browser tab with your client Codespace

2. **Stop the Current Client** (if it's running):
   - Press Ctrl+C in the terminal to stop the client
   - Wait for it to shut down completely

3. **Start the Client with Verbose Logging**:
   - Type the following command and press Enter:
   ```bash
   python track_client.py --verbose
   ```
   - This starts the client with more detailed logging

4. **Explain the Verbose Output**:
   - Point out the additional debug information
   - Show the exact request being sent to the server
   - Highlight the location data in the request

### 7.3 Observe the Communication

1. **Switch Between Codespaces**:
   - Go back to the server Codespace
   - Point out the new log entries that appeared when the client connected
   - Switch back to the client to show the corresponding output

2. **Explain the Request-Response Cycle**:
   - Client sends a request to the server
   - Server processes the request and updates the database
   - Server sends a response back to the client
   - Client processes the response and continues

3. **Refresh the Web Interface**:
   - Open the server URL in a browser tab
   - Navigate to the device details page
   - Refresh the page to show the updated location
   - Point out that the web interface reads from the same database that the client updates

## Step 8: Demonstrate Geofence Functionality

This step demonstrates the geofence feature, which is one of the key capabilities of the application.

### 8.1 Create a Geofence for Testing

1. **Access the Device Details Page**:
   - In your browser, make sure you're on the device details page
   - If not, go to the dashboard and click "View Details" for your device

2. **Create a Strategic Geofence**:
   - Click the "Add Geofence" button
   - A modal window will appear
   - Fill in the geofence details:
     - Name: `Mumbai Office`
     - Latitude: `19.0760` (use the exact Mumbai coordinates)
     - Longitude: `72.8777`
     - Radius: `0.2` (small radius to make it easier to trigger violations)
   - Click the "Save Geofence" button

3. **Explain the Geofence**:
   - Point out the circular geofence on the map
   - Explain that the radius is 0.2 kilometers (200 meters)
   - Show that the current device location is inside the geofence

### 8.2 Modify the Client for Testing

1. **Switch to the Client Codespace**:
   - Go to the browser tab with your client Codespace

2. **Stop the Current Client**:
   - Press Ctrl+C in the terminal to stop the client

3. **Create a Test Script for Location Simulation**:
   - Open a new file in the editor:
   ```bash
   code test_locations.py
   ```
   - Paste the following code:
   ```python
   # Add this to the client for simulating movement within and outside Mumbai
   def get_test_locations():
       # Locations inside and outside the geofence
       locations = [
           {"latitude": 19.0760, "longitude": 72.8777, "city": "Mumbai", "area": "Office", "status": "Inside geofence"},
           {"latitude": 19.0821, "longitude": 72.8416, "city": "Mumbai", "area": "Andheri", "status": "Outside geofence"},
           {"latitude": 19.0760, "longitude": 72.8777, "city": "Mumbai", "area": "Office", "status": "Back inside geofence"}
       ]

       for i, location in enumerate(locations):
           print(f"\nLocation {i+1}: {location['area']} - {location['status']}")
           print(f"Latitude: {location['latitude']}, Longitude: {location['longitude']}")

           # Add common fields
           location["ip"] = "103.168.233.10"
           location["region"] = "Maharashtra"
           location["country"] = "India"

           # Ask user to press Enter to continue
           input("Press Enter to send this location update...")

           # Here you would normally send the location to the server
           # For demo purposes, just print what would be sent
           print(f"Sending update to server: {location}")

   # Run the function
   if __name__ == "__main__":
       print("Location Test Utility")
       print("====================\n")
       print("This script will simulate device movement for testing geofence alerts.")
       print("You'll need to manually update the location in the real client after each step.")
       input("Press Enter to begin...")
       get_test_locations()
   ```
   - Save the file (Ctrl+S)

4. **Run the Test Script**:
   ```bash
   python test_locations.py
   ```
   - This will guide you through the test locations

### 8.3 Demonstrate Geofence Violations

1. **Follow the Test Script Prompts**:
   - The script will show the first location (inside the geofence)
   - Press Enter to continue

2. **Manually Update the Client Location**:
   - In a new terminal tab, run the client with the coordinates from the test script:
   ```bash
   # For the first location (inside geofence)
   python track_client.py --latitude 19.0760 --longitude 72.8777
   ```
   - Let it run for a moment, then press Ctrl+C to stop it

3. **Check the Web Interface**:
   - Refresh the device details page
   - Verify the location is shown correctly
   - Note that there are no geofence alerts

4. **Move Outside the Geofence**:
   - Go back to the test script and press Enter for the next location
   - Run the client with the new coordinates:
   ```bash
   # For the second location (outside geofence)
   python track_client.py --latitude 19.0821 --longitude 72.8416
   ```

5. **Show the Geofence Alert**:
   - Refresh the device details page
   - Point out the geofence violation alert that appears
   - Explain that this would trigger notifications in a production system

6. **Return Inside the Geofence**:
   - Continue with the test script for the third location
   - Run the client with the original coordinates:
   ```bash
   # For the third location (back inside geofence)
   python track_client.py --latitude 19.0760 --longitude 72.8777
   ```
   - Refresh the web interface to show that the alert is no longer active

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

## Advanced: Simulating Different Locations in India

To make the demo more interesting and relevant to an Indian context, you can simulate different locations across India in the client:

1. Modify the client code to use fixed coordinates for Mumbai instead of IP-based geolocation:

```python
# Add this function to the client
def get_mock_location():
    # Mumbai coordinates
    return {
        "ip": "103.168.233.1",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "city": "Mumbai",
        "region": "Maharashtra",
        "country": "India"
    }

# Use this function instead of the real geolocation
```

2. Create a sequence of locations to simulate movement across major Indian cities:

```python
# Add this to the client
def get_mock_location_sequence():
    locations = [
        {"latitude": 19.0760, "longitude": 72.8777, "city": "Mumbai", "region": "Maharashtra"},
        {"latitude": 28.6139, "longitude": 77.2090, "city": "Delhi", "region": "Delhi"},
        {"latitude": 12.9716, "longitude": 77.5946, "city": "Bengaluru", "region": "Karnataka"},
        {"latitude": 17.3850, "longitude": 78.4867, "city": "Hyderabad", "region": "Telangana"},
        {"latitude": 22.5726, "longitude": 88.3639, "city": "Kolkata", "region": "West Bengal"},
        {"latitude": 13.0827, "longitude": 80.2707, "city": "Chennai", "region": "Tamil Nadu"},
        {"latitude": 23.0225, "longitude": 72.5714, "city": "Ahmedabad", "region": "Gujarat"},
        {"latitude": 18.5204, "longitude": 73.8567, "city": "Pune", "region": "Maharashtra"}
    ]

    # Return a different location each time
    import time
    index = int(time.time() / 60) % len(locations)
    location = locations[index]
    location["ip"] = "103.168.233." + str(index + 1)  # Simulate different IPs
    location["country"] = "India"
    return location
```

3. For a more realistic demo, you can simulate movement within Mumbai to demonstrate geofence capabilities:

```python
# Add this to the client for simulating movement within Mumbai
def get_mumbai_movement_sequence():
    # Various locations within Mumbai
    locations = [
        {"latitude": 19.0760, "longitude": 72.8777, "city": "Mumbai", "area": "City Center"},
        {"latitude": 19.0178, "longitude": 72.8478, "city": "Mumbai", "area": "Bandra"},
        {"latitude": 19.0821, "longitude": 72.8416, "city": "Mumbai", "area": "Andheri"},
        {"latitude": 19.0330, "longitude": 73.0297, "city": "Mumbai", "area": "Navi Mumbai"},
        {"latitude": 18.9548, "longitude": 72.8224, "city": "Mumbai", "area": "Colaba"},
        {"latitude": 19.1759, "longitude": 72.9482, "city": "Mumbai", "area": "Thane"}
    ]

    # Return a different location every 30 seconds
    import time
    index = int(time.time() / 30) % len(locations)
    location = locations[index]
    location["ip"] = "103.168.233.10"
    location["region"] = "Maharashtra"
    location["country"] = "India"
    return location
```

This will create a more dynamic demonstration of the tracking and geofencing capabilities with familiar Indian locations. When setting up geofences for the demo, you can use Mumbai's coordinates as the center point and set a radius that would trigger alerts when the simulated device moves to other areas within Mumbai or to other cities in India.
