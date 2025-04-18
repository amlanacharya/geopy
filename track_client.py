#!/usr/bin/env python3
import requests
import socket
import platform
import time
import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
import uuid
import configparser
import argparse

# Setup logging
log_dir = os.path.join(os.path.expanduser("~"), ".laptop_tracker")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "client.log")
log_dir = os.path.join(os.path.expanduser("~"), ".laptop_tracker")
os.makedirs(log_dir, exist_ok=True)
config_file = os.path.join(log_dir, "config.ini")

logger = logging.getLogger("LaptopTracker")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



class DeviceTracker:
    def __init__(self, server_url, username, password, update_interval=300):
        """Initialize the device tracker client"""
        self.server_url = server_url
        self.username = username
        self.password = password
        self.update_interval = update_interval
        self.device_id = None
        self.hostname = socket.gethostname()
        self.os_info = platform.platform()
        self.client_id = self._get_client_id()
    
    def _get_client_id(self):
        """Get or create a unique client ID"""
        client_id_file = os.path.join(log_dir, "client_id")
        
        if os.path.exists(client_id_file):
            try:
                with open(client_id_file, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Error reading client ID: {e}")
        
        # Generate new client ID
        client_id = str(uuid.uuid4())
        try:
            with open(client_id_file, 'w') as f:
                f.write(client_id)
            # Set file permissions to be readable only by the user
            os.chmod(client_id_file, 0o600)
        except Exception as e:
            logger.error(f"Error saving client ID: {e}")
        
        return client_id
    
    def register_device(self):
        """Register the device with the server"""
        logger.info("Registering device with the server...")
        
        try:
            response = requests.post(
                f"{self.server_url}/api/client/register",
                json={
                    "username": self.username,
                    "password": self.password,
                    "hostname": self.hostname,
                    "os_info": self.os_info,
                    "client_id": self.client_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    self.device_id = data.get("device_id")
                    logger.info(f"Device registered successfully with ID: {self.device_id}")
                    return True
                else:
                    logger.error(f"Registration failed: {data.get('message')}")
            else:
                logger.error(f"Registration failed with status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during device registration: {e}")
        
        return False
    
    def get_location(self):

        """Get the current location using IP-based geolocation services"""
        logger.info("Getting current location...")
        
        # Try multiple geolocation APIs in case one fails
        apis = [
            "https://ipapi.co/json/",
            "https://ipinfo.io/json",  # May require a token for production use
            "https://ip-api.com/json"
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    location_data = response.json()
                    
                    # Handle different API response formats
                    if api_url.startswith("https://ipapi.co"):
                        return {
                            "latitude": location_data.get("latitude"),
                            "longitude": location_data.get("longitude"),
                            "ip_address": location_data.get("ip"),
                            "city": location_data.get("city"),
                            "region": location_data.get("region"),
                            "country": location_data.get("country_name")
                        }
                    elif api_url.startswith("https://ipinfo.io"):
                        # ipinfo uses loc field with format "lat,lng"
                        if "loc" in location_data and "," in location_data["loc"]:
                            lat, lng = location_data["loc"].split(",")
                            return {
                                "latitude": float(lat),
                                "longitude": float(lng),
                                "ip_address": location_data.get("ip"),
                                "city": location_data.get("city"),
                                "region": location_data.get("region"),
                                "country": location_data.get("country")
                            }
                    elif api_url.startswith("https://ip-api.com"):
                        return {
                            "latitude": location_data.get("lat"),
                            "longitude": location_data.get("lon"),
                            "ip_address": location_data.get("query"),
                            "city": location_data.get("city"),
                            "region": location_data.get("regionName"),
                            "country": location_data.get("country")
                        }
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error getting location from {api_url}: {e}")
        
        logger.error("All geolocation APIs failed, using fallback coordinates")
        
        # Fallback to minimal location data
        return {
            "latitude": 0,
            "longitude": 0,
            "ip_address": None,
            "city": None,
            "region": None,
            "country": None
        }
    
    def update_location(self):
        """Send location update to the server"""
        if not self.device_id:
            if not self.register_device():
                logger.error("Cannot update location: device is not registered")
                return False
        
        location = self.get_location()
        if not location:
            logger.error("Cannot update location: failed to get current location")
            return False
        
        logger.info("Sending location update to server...")
        try:
            # Add the device_id to the location data
            location["device_id"] = self.device_id
            
            response = requests.post(
                f"{self.server_url}/api/update_location",
                json=location,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    logger.info("Location updated successfully")
                    return True
                else:
                    logger.error(f"Location update failed: {data.get('message')}")
            else:
                logger.error(f"Location update failed with status code: {response.status_code}")
                
                # If device not found, try re-registering
                if response.status_code == 404:
                    logger.info("Device not found on server, attempting to re-register...")
                    if self.register_device():
                        # Try updating again
                        return self.update_location()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during location update: {e}")
        
        return False
    
    def run(self):
        """Main loop to periodically update the location"""
        logger.info("Starting device tracker client...")
        
        if not self.register_device():
            logger.error("Failed to register device, will retry on first update")
        
        while True:
            try:
                self.update_location()
            except Exception as e:
                logger.error(f"Unexpected error during location update: {e}")
            
            logger.info(f"Sleeping for {self.update_interval} seconds...")
            time.sleep(self.update_interval)

def create_default_config():
    """Create a default configuration file if it doesn't exist"""
    if not os.path.exists(config_file):
        logger.info("Creating default configuration file...")
        config = configparser.ConfigParser()
        config['SERVER'] = {
            'URL': 'http://localhost:5000',
            'UpdateInterval': '300'
        }
        config['USER'] = {
            'Username': '',
            'Password': ''
        }
        
        try:
            with open(config_file, 'w') as f:
                config.write(f)
            # Set file permissions to be readable only by the user
            os.chmod(config_file, 0o600)
            logger.info(f"Default configuration file created at {config_file}")
            print(f"Default configuration file created at {config_file}")
            print("Please edit the file to add your username and password.")
        except Exception as e:
            logger.error(f"Error creating configuration file: {e}")
            print(f"Error creating configuration file: {e}")
    
def load_config():
    """Load configuration from file"""
    if not os.path.exists(config_file):
        create_default_config()
        return None
    
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return {
            'server_url': config.get('SERVER', 'URL'),
            'username': config.get('USER', 'Username'),
            'password': config.get('USER', 'Password'),
            'update_interval': config.getint('SERVER', 'UpdateInterval')
        }
    except (configparser.Error, ValueError) as e:
        logger.error(f"Error parsing configuration file: {e}")
        print(f"Error parsing configuration file: {e}")
        return None

def main():
    """Main entry point"""
    global config_file

    parser = argparse.ArgumentParser(description='Laptop Tracking Client')
    parser.add_argument('--server', help='Server URL', default=None)
    parser.add_argument('--user', help='Username', default=None)
    parser.add_argument('--password', help='Password', default=None)
    parser.add_argument('--interval', help='Update interval in seconds', type=int, default=None)
    parser.add_argument('--config', help='Path to configuration file', default=config_file)
    
    args = parser.parse_args()
    # Load configuration
    if args.config != config_file:
        
        config_file = args.config
    
    config = load_config()
    if not config:
        print("Please configure the client before running.")
        return
    
    # Command line arguments override configuration file
    server_url = args.server or config['server_url']
    username = args.user or config['username']
    password = args.password or config['password']
    update_interval = args.interval or config['update_interval']
    
    # Validate configuration
    if not server_url or not username or not password:
        print("Missing required configuration: server URL, username, and password must be provided.")
        return
    
    # Create and run the tracker
    tracker = DeviceTracker(server_url, username, password, update_interval)
    
    # Handle graceful exit
    try:
        tracker.run()
    except KeyboardInterrupt:
        print("Stopping device tracker client...")
        logger.info("Device tracker client stopped by user")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()