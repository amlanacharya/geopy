# Find My Laptop - Demo Guide

This guide will walk you through running and demonstrating the Find My Laptop application on a single device. No prior knowledge is required.

## What is Find My Laptop?

Find My Laptop is a secure, self-hosted application that allows you to:
- Track the location of your devices
- Set up geofences (virtual boundaries)
- Get alerts when your devices move outside these boundaries
- View location history

## Prerequisites

- Python 3.6 or higher installed on your computer
- A web browser (Chrome, Firefox, Edge, etc.)
- Basic knowledge of using the command line/terminal

## Step 1: Download the Application

If you haven't already, download the application files from the repository.

## Step 2: Start the Server

1. Open a command prompt or terminal window
2. Navigate to the folder containing the application files
3. Run the following command to start the server:

```bash
python track_server.py
```

4. You should see output similar to:

```
* Serving Flask app 'track_server'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://192.168.x.x:5000
```

5. Keep this window open while using the application

## Step 3: Access the Web Interface

1. Open your web browser
2. Navigate to: http://localhost:5000
3. You should see the Find My Laptop landing page with Login and Register buttons

## Step 4: Create an Account

1. Click the "Register" button
2. Fill in the registration form:
   - Username: Choose any username (e.g., "demo_user")
   - Password: Create a password (at least 8 characters)
   - Confirm Password: Enter the same password again
3. Click "Register"
4. You'll be redirected to the login page

## Step 5: Log In

1. Enter the username and password you just created
2. Click "Login"
3. You'll be redirected to the dashboard

## Step 6: Add a Device Manually

1. On the dashboard, click the "Add Device" button
2. A popup window will appear
3. Enter a device name (e.g., "My Laptop")
4. Select a device type from the dropdown (e.g., "Laptop")
5. Click "Register Device"
6. The page will refresh and your new device will appear in the list

## Step 7: View Device Details

1. Click "View Details" next to the device you just added
2. You'll see the device details page, which currently has no location data

## Step 8: Add a Geofence

1. On the device details page, click the "Add Geofence" button
2. A popup window will appear
3. Fill in the geofence details:
   - Name: Enter a name for the location (e.g., "Home")
   - Latitude: Enter a latitude value (e.g., 40.7128 for New York)
   - Longitude: Enter a longitude value (e.g., -74.0060 for New York)
   - Radius: Enter a radius in kilometers (e.g., 1.0)
4. Click "Save Geofence"
5. The page will refresh and your new geofence will appear in the list

## Step 9: Run the Client Application

Now, let's simulate a device sending its location to the server.

1. Open a new command prompt or terminal window (keep the server running in the first window)
2. Navigate to the folder containing the application files
3. Run the following command to start the client:

```bash
python track_client.py --server http://localhost:5000 --user demo_user --password yourpassword
```

Replace `demo_user` with your username and `yourpassword` with your actual password.

4. The client will start sending location updates to the server
5. You should see output indicating successful registration and location updates

## Step 10: View Location Updates

1. Go back to your browser
2. Refresh the device details page
3. You should now see location information for your device
4. If the location is outside the geofence you created, you'll see an alert

## Step 11: Explore the Features

Now that you have the basic setup working, explore the application:

1. **Dashboard**: Shows all your registered devices
2. **Device Details**: Shows location history and geofences for a specific device
3. **Geofences**: Virtual boundaries that trigger alerts when crossed

## Troubleshooting

### Server Issues

- Make sure no other application is using port 5000
- Check the server terminal for error messages
- Try restarting the server

### Client Issues

- Verify your username and password
- Make sure the server is running
- Check the client terminal for error messages

### Browser Issues

- Try clearing your browser cache
- Use incognito/private browsing mode
- Try a different browser

## Shutting Down

When you're done with the demo:

1. Press Ctrl+C in the client terminal to stop the client
2. Press Ctrl+C in the server terminal to stop the server

## Next Steps

- Try running the client on a different device on the same network
- Set up the application on a server for remote access
- Explore the code to understand how it works

## Security Note

This application is designed for educational purposes. For real-world use:
- Use HTTPS for secure communication
- Host on a properly secured server
- Regularly update dependencies
