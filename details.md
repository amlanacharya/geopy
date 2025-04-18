# Find My Laptop - Project Report

## Executive Summary

The "Find My Laptop" project is a comprehensive device tracking system designed to help users locate and secure their devices. This application provides a secure, self-hosted solution with features such as real-time location tracking, geofencing capabilities, location history, and device management through a responsive web interface. The primary goal of this project is to develop a privacy-focused alternative to commercial tracking solutions that gives users full control over their data.

## 1. Introduction

### 1.1 Problem Statement

Device theft and loss continue to be significant concerns for individuals and organizations. While commercial tracking solutions exist, they often come with privacy concerns, subscription fees, and limited customization options. There is a need for an open, secure, and self-hosted tracking solution that can be deployed in educational and organizational environments without compromising user privacy or requiring ongoing costs.

### 1.2 Project Objectives

- Develop a client-server tracking application that securely monitors device locations
- Implement a robust user authentication system with security best practices
- Create an intuitive web-based dashboard for device management
- Build a lightweight client application to run on tracked devices
- Incorporate geofencing capabilities with alert potential
- Provide location history visualization for tracked devices
- Ensure data privacy through a self-hosted approach

### 1.3 Scope

The project encompasses both server and client components:

- **Server**: A Flask-based web application with a secure user interface, database storage, and API endpoints
- **Client**: A Python application that runs on tracked devices to report location data
- **Features**: User registration/login, device management, location tracking, geofencing, and location history

## 2. System Architecture

### 2.1 High-Level Architecture

The system follows a client-server architecture with the following components:

1. **Server Component**: Flask-based web application providing user interfaces and API endpoints
2. **Client Component**: Python application for location reporting installed on tracked devices
3. **Database**: SQLite database for data storage
4. **Front-end**: HTML/CSS/JavaScript for the user interface

### 2.2 Database Schema

The system uses an SQLite database with the following structure:

- **Users Table**: Stores user credentials and authentication information
  - id (primary key)
  - username
  - password (hashed)
  - salt

- **Devices Table**: Stores information about registered devices
  - id (primary key)
  - user_id (foreign key to Users)
  - device_name
  - device_type
  - registered_date

- **Locations Table**: Stores location history for devices
  - id (primary key)
  - device_id (foreign key to Devices)
  - latitude
  - longitude
  - ip_address
  - city
  - region
  - country
  - timestamp

- **Geofences Table**: Stores geofencing information for alerts
  - id (primary key)
  - device_id (foreign key to Devices)
  - latitude
  - longitude
  - radius
  - name

### 2.3 Communication Flow

1. **User Registration/Login**: Users register and log in through the web interface
2. **Device Registration**: 
   - Manual: Users can manually register devices through the web interface
   - Automatic: Client applications can register devices programmatically
3. **Location Updating**:
   - The client periodically collects location data
   - The client sends location updates to the server API
   - The server stores location updates in the database
4. **Device Monitoring**:
   - Users view device locations through the web dashboard
   - The server checks for geofence violations
   - Users can view location history for any device

## 3. Technical Implementation

### 3.1 Server Implementation

The server is implemented using Flask, a lightweight Python web framework. Key components include:

#### 3.1.1 User Authentication System

- Secure user registration with salted password hashing
- Login system with session management
- CSRF protection for all forms and API requests

#### 3.1.2 Web Interface

- Responsive dashboard for device management
- Interactive maps for visualizing device locations
- Forms for adding devices and setting geofences
- Device detail pages with location history

#### 3.1.3 API Endpoints

- `/api/register_device`: Registers a new device
- `/api/update_location`: Updates device location
- `/api/add_geofence`: Adds a new geofence
- `/api/client/register`: Endpoint for client applications to register devices

#### 3.1.4 Security Features

- Password hashing with SHA-256 and random salts
- CSRF protection for all forms and API endpoints
- Content Security Policy (CSP) implementation
- Input validation and sanitization
- Session security with random tokens

### 3.2 Client Implementation

The client is a Python application designed to be lightweight and unobtrusive. Key features include:

#### 3.2.1 Configuration Management

- Local config file for storing credentials and settings
- Command-line arguments for overriding configuration
- Secure credential storage with proper file permissions

#### 3.2.2 Location Services

- IP-based geolocation using public APIs
- Multiple API fallbacks for reliability
- Location caching to reduce API requests

#### 3.2.3 Communication with Server

- Secure HTTP requests to server API endpoints
- Authentication using stored credentials
- Automatic retry mechanism for connection failures
- Periodic updates based on configurable intervals

#### 3.2.4 Logging and Diagnostics

- Rotating log files for tracking operations
- Error handling with informative messages
- Configurable logging levels

### 3.3 Security Considerations

The project implements several security measures:

- **Authentication**: Password hashing with random salts
- **CSRF Protection**: Token-based CSRF protection for all forms
- **Content Security Policy**: Limiting resource loading to trusted sources
- **Input Validation**: Server-side validation of all inputs
- **File Permissions**: Secure permissions for configuration and credential files
- **Error Handling**: Non-revealing error messages to prevent information leakage

## 4. Implementation Challenges and Solutions

### 4.1 Challenges Faced

#### 4.1.1 IP-Based Geolocation Limitations

**Challenge**: IP-based geolocation lacks pinpoint accuracy and sometimes returns default coordinates (0.0, 0.0).

**Solution**: Implemented multiple geolocation API fallbacks and added better error handling to improve reliability. The system also allows for manual location entry through the web interface.

#### 4.1.2 Cross-Origin Resource Sharing in Codespaces

**Challenge**: Testing in environments like GitHub Codespaces introduced CORS and server accessibility issues.

**Solution**: Added proper port forwarding configuration and updated the client to work with HTTPS connections. Additionally, improved documentation for testing in containerized environments.

#### 4.1.3 Security vs. Usability Balance

**Challenge**: Balancing strong security measures with user experience.

**Solution**: Implemented a tiered approach where critical security features (password hashing, CSRF protection) are non-negotiable, while allowing flexibility in other areas. The user interface was designed to make secure operations straightforward.

### 4.2 Technical Debt and Future Improvements

The following areas have been identified for future improvements:

- **Alternative Location Methods**: Integrate GPS and WiFi-based location for better accuracy
- **Mobile Application**: Develop mobile clients for iOS and Android
- **Real-time Alerts**: Implement real-time notifications for geofence violations
- **Data Encryption**: Add end-to-end encryption for location data
- **Performance Optimization**: Optimize database queries for better scalability

## 5. Testing and Deployment

### 5.1 Testing Methodology

The application was tested using the following approaches:

- **Unit Testing**: Testing individual functions and classes
- **Integration Testing**: Testing API endpoints and database operations
- **End-to-End Testing**: Testing the complete workflow from client to server
- **Security Testing**: Testing for common vulnerabilities (XSS, CSRF, SQL Injection)
- **Cross-Platform Testing**: Testing on different operating systems

### 5.2 Deployment Strategy

The application is designed for flexibility in deployment:

- **Development**: Local deployment using Flask's built-in server
- **Testing**: Containerized deployment using GitHub Codespaces
- **Production**: Deployment options include:
  - Traditional hosting with WSGI servers (Gunicorn, uWSGI)
  - Container-based deployment (Docker)
  - Self-hosted on premises

### 5.3 Maintenance Considerations

For ongoing maintenance, the following practices are recommended:

- Regular security updates
- Database backups
- Log rotation and monitoring
- User credential management
- Periodic security audits

## 6. User Guide

### 6.1 Server Setup

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install required packages: `pip install flask requests`
4. Run the server: `python track_server.py`

### 6.2 Client Setup

1. Install required packages: `pip install requests`
2. Configure the client by editing `~/.laptop_tracker/config.ini`
3. Run the client: `python track_client.py`

### 6.3 Using the Web Interface

1. **Registration and Login**:
   - Access the web interface at `http://server-ip:5000`
   - Register a new account
   - Log in with your credentials

2. **Managing Devices**:
   - View your devices on the dashboard
   - Add new devices manually
   - Click on a device to view its details

3. **Setting Geofences**:
   - Navigate to the device details page
   - Click "Add Geofence"
   - Enter a name, coordinates, and radius
   - Save the geofence

4. **Viewing Location History**:
   - Open the device details page
   - Scroll down to see the location history
   - The map shows the current location and all geofences

## 7. Conclusion

### 7.1 Summary of Achievements

The "Find My Laptop" project successfully delivers:

- A secure, self-hosted tracking solution
- A user-friendly web interface for device management
- A lightweight client for location reporting
- Geofencing capabilities for setting boundaries
- Comprehensive location history
- A robust security model protecting user data

### 7.2 Learning Outcomes

This project provided valuable experience in:

- Full-stack web development with Flask
- Client-server application architecture
- Secure authentication implementation
- Geographic data handling and visualization
- Cross-platform Python application development
- Security best practices for web applications

### 7.3 Future Directions

Based on the current implementation, several future directions are promising:

- Mobile client applications for broader device support
- Enhanced location accuracy using multiple methods
- Real-time notifications using WebSockets
- Administration interfaces for organizational use
- API enhancements for third-party integration
- Machine learning for predictive location analysis and theft detection

## Appendices

### Appendix A: Code Repository Structure

```
find-my-laptop/
├── track_server.py       # Server implementation
├── track_client.py       # Client implementation
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # User dashboard
│   └── device.html       # Device details page
├── .gitignore            # Git ignore file
└── README.md             # Project documentation
```

### Appendix B: API Documentation

#### B.1 `/api/register_device` (POST)

Registers a new device for the authenticated user.

**Request:**
```json
{
  "device_name": "string",
  "device_type": "string",
  "csrf_token": "string"
}
```

**Response:**
```json
{
  "status": "success|error",
  "device_id": "integer",
  "message": "string"
}
```

#### B.2 `/api/update_location` (POST)

Updates the location of a registered device.

**Request:**
```json
{
  "device_id": "integer",
  "latitude": "float",
  "longitude": "float",
  "ip_address": "string",
  "city": "string",
  "region": "string",
  "country": "string"
}
```

**Response:**
```json
{
  "status": "success|error",
  "message": "string"
}
```

#### B.3 `/api/add_geofence` (POST)

Adds a geofence for a registered device.

**Request:**
```json
{
  "device_id": "integer",
  "name": "string",
  "latitude": "float",
  "longitude": "float",
  "radius": "float",
  "csrf_token": "string"
}
```

**Response:**
```json
{
  "status": "success|error",
  "message": "string"
}
```

#### B.4 `/api/client/register` (POST)

Registers a device from the client application.

**Request:**
```json
{
  "username": "string",
  "password": "string",
  "hostname": "string",
  "os_info": "string",
  "client_id": "string"
}
```

**Response:**
```json
{
  "status": "success|error",
  "device_id": "integer",
  "message": "string"
}
```

### Appendix C: References

- Flask Documentation: https://flask.palletsprojects.com/
- Python Requests Library: https://docs.python-requests.org/
- Leaflet.js for Maps: https://leafletjs.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- OWASP Web Security: https://owasp.org/www-project-web-security-testing-guide/
