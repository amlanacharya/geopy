# Find My Laptop

A secure, self-hosted laptop tracking solution developed as a college project. This application allows users to track their devices, set geofences, and get alerts when devices move outside designated areas.

## Features

- **Secure User Management**: Register and login with salted password hashing
- **Device Tracking**: Track the location of multiple devices
- **Geofencing**: Set up virtual boundaries and receive alerts when devices leave these areas
- **Location History**: View the history of device locations
- **Client-Server Architecture**: Separate client for devices and server for the web interface

## System Requirements

- Python 3.6 or higher
- Internet connection

## Installation

### Server Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/find-my-laptop.git
   cd find-my-laptop
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install flask requests
   ```

4. Run the server:
   ```bash
   python track_server.py
   ```

The server will be accessible at `http://localhost:5000`

### Client Setup

1. Install required packages:
   ```bash
   pip install requests
   ```

2. Configure the client:
   - Edit the configuration file at `~/.laptop_tracker/config.ini` or create it with:
     ```ini
     [SERVER]
     URL = http://your-server-url:5000
     UpdateInterval = 300
     
     [USER]
     Username = your_username
     Password = your_password
     ```

3. Run the client:
   ```bash
   python track_client.py
   ```

Alternatively, provide credentials directly:
```bash
python track_client.py --server http://your-server-url:5000 --user username --password password
```

## Usage

1. Register a new account on the web interface
2. Log in to access your dashboard
3. Add devices manually or run the client on your devices
4. Set up geofences for your devices
5. Monitor your devices' locations through the dashboard

## Development

### Directory Structure

- `track_server.py`: Main server application
- `track_client.py`: Client application for devices
- `templates/`: HTML templates for the web interface
- `.gitignore`: Git ignore file

### Server Components

- Flask web application
- SQLite database for data storage
- User authentication system
- API endpoints for client communication

### Client Components

- Location detection using IP geolocation
- Automatic device registration
- Periodic location updates

## Testing in GitHub Codespaces

If you're running this application in GitHub Codespaces:

1. Run the server in one terminal:
   ```bash
   python track_server.py
   ```

2. Configure port forwarding:
   - Go to the "Ports" tab
   - Make port 5000 public

3. Get the public URL for your server (e.g., `https://username-project-abc123.app.github.dev`)

4. Run the client in another terminal using the public URL:
   ```bash
   python track_client.py --server https://username-project-abc123.app.github.dev --user username --password password
   ```

## Security Considerations

- Use HTTPS in production
- Keep your server behind a proper firewall
- Regularly update passwords
- Don't expose the server directly to the internet without proper security measures

## License

This project is intended for educational purposes only.

## Troubleshooting

### Client can't connect to server
- Verify the server URL is correct
- Ensure the username and password are valid
- Check if the server is running and accessible

### Location updates not appearing
- Check client logs at `~/.laptop_tracker/client.log`
- Verify network connectivity
- Refresh the dashboard page

### Registration errors
- Ensure username is unique
- Make sure password meets strength requirements
