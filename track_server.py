import sqlite3
import datetime
import os
import math
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import json
import hashlib
from functools import wraps
import secrets
import threading

app = Flask(__name__)
# Use a fixed secret key from an environment variable or generate once and save
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

class DatabaseManager:
    def __init__(self, db_name='device_tracker.db'):
        """Initialize database connection and setup tables"""
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Add mutex for thread safety
        self.lock = threading.Lock()
        self.setup_database()

    def setup_database(self):
        """Create necessary tables if they don't exist"""
        with self.lock:
            # Users table - Add salt column for password security
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
            ''')
            
            # Rest of the tables remain the same
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                device_name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                registered_date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY,
                device_id INTEGER,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                ip_address TEXT,
                city TEXT,
                region TEXT,
                country TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS geofences (
                id INTEGER PRIMARY KEY,
                device_id INTEGER,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                radius REAL NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
            ''')
            
            self.conn.commit()
    
    def register_user(self, username, password):
        """Register a new user with salted password"""
        with self.lock:
            # Generate a random salt
            salt = secrets.token_hex(16)
            # Hash the password with the salt
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            
            try:
                self.cursor.execute(
                    "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
                    (username, hashed_password, salt)
                )
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def verify_user(self, username, password):
        """Verify user credentials using salted password"""
        with self.lock:
            # Get the user's salt
            self.cursor.execute("SELECT id, password, salt FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            
            if not result:
                return None
                
            user_id, stored_hash, salt = result
            # Compute the hash with the provided password and stored salt
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            
            # Compare the computed hash with the stored hash
            if hashed_password == stored_hash:
                return user_id
            return None
    
    # Other methods remain similar but use the lock for thread safety
    def register_device(self, user_id, device_name, device_type):
        """Register a new device for a user"""
        with self.lock:
            try:
                self.cursor.execute(
                    "INSERT INTO devices (user_id, device_name, device_type, registered_date) VALUES (?, ?, ?, ?)",
                    (user_id, device_name, device_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                self.conn.commit()
                return self.cursor.lastrowid
            except Exception as e:
                print(f"Error registering device: {str(e)}")
                return None
    
    def get_user_devices(self, user_id):
        """Get all devices for a user"""
        with self.lock:
            self.cursor.execute(
                "SELECT id, device_name, device_type, registered_date FROM devices WHERE user_id = ?",
                (user_id,)
            )
            return self.cursor.fetchall()
    
    def get_device_details(self, device_id):
        """Get device details"""
        with self.lock:
            self.cursor.execute(
                "SELECT d.id, d.device_name, d.device_type, d.registered_date, u.username "
                "FROM devices d JOIN users u ON d.user_id = u.id WHERE d.id = ?",
                (device_id,)
            )
            return self.cursor.fetchone()
    
    def update_device_location(self, device_id, latitude, longitude, ip_address=None, 
                              city=None, region=None, country=None):
        """Update the location of a device"""
        with self.lock:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO locations (device_id, latitude, longitude, ip_address, city, region, country, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (device_id, latitude, longitude, ip_address, city, region, country, timestamp)
            )
            self.conn.commit()
            
            # Check geofences
            self.check_geofences(device_id, latitude, longitude)
            
            return True
    
    def get_device_location_history(self, device_id, limit=20):
        """Get the location history for a device"""
        with self.lock:
            self.cursor.execute(
                "SELECT latitude, longitude, ip_address, city, region, country, timestamp "
                "FROM locations WHERE device_id = ? ORDER BY timestamp DESC LIMIT ?",
                (device_id, limit)
            )
            return self.cursor.fetchall()
    
    def get_latest_device_location(self, device_id):
        """Get the latest location for a device"""
        with self.lock:
            self.cursor.execute(
                "SELECT latitude, longitude, ip_address, city, region, country, timestamp "
                "FROM locations WHERE device_id = ? ORDER BY timestamp DESC LIMIT 1",
                (device_id,)
            )
            return self.cursor.fetchone()
    
    def add_geofence(self, device_id, name, latitude, longitude, radius):
        """Add a geofence for a device"""
        with self.lock:
            self.cursor.execute(
                "INSERT INTO geofences (device_id, latitude, longitude, radius, name) VALUES (?, ?, ?, ?, ?)",
                (device_id, latitude, longitude, radius, name)
            )
            self.conn.commit()
            return True
    
    def get_device_geofences(self, device_id):
        """Get all geofences for a device"""
        with self.lock:
            self.cursor.execute(
                "SELECT id, name, latitude, longitude, radius FROM geofences WHERE device_id = ?",
                (device_id,)
            )
            return self.cursor.fetchall()
    
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on earth (specified in decimal degrees)"""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def check_geofences(self, device_id, latitude, longitude):
        """Check if a device is outside any of its geofences using Haversine formula"""
        with self.lock:
            geofences = self.get_device_geofences(device_id)
            alerts = []
            
            for geofence in geofences:
                geo_id, name, geo_lat, geo_lon, radius = geofence
                
                # Calculate distance using Haversine formula
                distance = self.haversine_distance(latitude, longitude, geo_lat, geo_lon)
                
                if distance > radius:
                    # Device is outside the geofence
                    device = self.get_device_details(device_id)
                    if device:
                        device_name = device[1]
                        alerts.append({
                            "device_id": device_id,
                            "device_name": device_name,
                            "geofence_name": name,
                            "distance": distance,
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
            
            return alerts

# Initialize database
db = DatabaseManager()

# Flask routes with CSRF protection added
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Add CSRF protection function
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

# Make csrf_token available to all templates
@app.context_processor
def inject_csrf_token():
    return {'csrf_token': generate_csrf_token()}

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # For form submissions, check CSRF token
        if not request.is_json:
            token = data.get('csrf_token')
            if not token or token != session.get('csrf_token'):
                return render_template('login.html', error="Invalid form submission, please try again"), 400
        
        username = data.get('username')
        password = data.get('password')
        
        user_id = db.verify_user(username, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            # Regenerate CSRF token on login
            session['csrf_token'] = secrets.token_hex(32)
            
            if request.is_json:
                return jsonify({"status": "success", "user_id": user_id})
            return redirect(url_for('dashboard'))
        
        if request.is_json:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

# Add CSRF checks to all other POST routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # For form submissions, check CSRF token
        if not request.is_json:
            token = data.get('csrf_token')
            if not token or token != session.get('csrf_token'):
                return render_template('register.html', error="Invalid form submission, please try again"), 400
        
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        # Server-side password confirmation check
        if not request.is_json and password != confirm_password:
            return render_template('register.html', error="Passwords do not match"), 400
        
        if db.register_user(username, password):
            if request.is_json:
                return jsonify({"status": "success"})
            return redirect(url_for('login'))
        
        if request.is_json:
            return jsonify({"status": "error", "message": "Username already exists"}), 400
        return render_template('register.html', error="Username already exists")
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('csrf_token', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    devices = db.get_user_devices(session['user_id'])
    return render_template('dashboard.html', devices=devices, username=session.get('username'))

@app.route('/device/<int:device_id>')
@login_required
def device_details(device_id):
    device = db.get_device_details(device_id)
    if not device or device[4] != session.get('username'):
        return redirect(url_for('dashboard'))
    
    latest_location = db.get_latest_device_location(device_id)
    history = db.get_device_location_history(device_id)
    geofences = db.get_device_geofences(device_id)
    
    return render_template('device.html', 
                          device=device, 
                          latest_location=latest_location,
                          history=history, 
                          geofences=geofences)

@app.route('/api/register_device', methods=['POST'])
@login_required
def api_register_device():
    data = request.get_json()
    
    # Check CSRF token for JSON requests from browser
    token = data.get('csrf_token')
    if token and token != session.get('csrf_token'):
        return jsonify({"status": "error", "message": "Invalid token"}), 400
    
    device_name = data.get('device_name')
    device_type = data.get('device_type')
    
    device_id = db.register_device(session['user_id'], device_name, device_type)
    if device_id:
        return jsonify({"status": "success", "device_id": device_id})
    return jsonify({"status": "error", "message": "Failed to register device"}), 400

@app.route('/api/update_location', methods=['POST'])
def api_update_location():
    data = request.get_json()
    device_id = data.get('device_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    ip_address = data.get('ip_address')
    city = data.get('city')
    region = data.get('region')
    country = data.get('country')
    
    # Verify the device exists
    device = db.get_device_details(device_id)
    if not device:
        return jsonify({"status": "error", "message": "Device not found"}), 404
    
    # Input validation
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Invalid coordinates")
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid coordinates"}), 400
    
    db.update_device_location(device_id, latitude, longitude, ip_address, city, region, country)
    return jsonify({"status": "success"})

@app.route('/api/add_geofence', methods=['POST'])
@login_required
def api_add_geofence():
    data = request.get_json()
    
    # Check CSRF token for JSON requests from browser
    token = data.get('csrf_token')
    if token and token != session.get('csrf_token'):
        return jsonify({"status": "error", "message": "Invalid token"}), 400
    
    device_id = data.get('device_id')
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    radius = data.get('radius')
    
    # Input validation
    try:
        device_id = int(device_id)
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Invalid coordinates")
        if radius <= 0:
            raise ValueError("Radius must be positive")
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid input data"}), 400
    
    # Verify the device belongs to the current user
    device = db.get_device_details(device_id)
    if not device or device[4] != session.get('username'):
        return jsonify({"status": "error", "message": "Device not found"}), 404
    
    if db.add_geofence(device_id, name, latitude, longitude, radius):
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Failed to add geofence"}), 400

# API endpoint for device registration from client
@app.route('/api/client/register', methods=['POST'])
def api_client_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    hostname = data.get('hostname')
    os_info = data.get('os_info')
    
    # Input validation
    if not all([username, password, hostname, os_info]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # Prevent header injection
    for field in [username, hostname, os_info]:
        if '\n' in field or '\r' in field:
            return jsonify({"status": "error", "message": "Invalid input"}), 400
    
    user_id = db.verify_user(username, password)
    if not user_id:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    
    # Check if device already exists for this user
    devices = db.get_user_devices(user_id)
    for device_id, name, device_type, _ in devices:
        if name == hostname:
            return jsonify({"status": "success", "device_id": device_id})
    
    # Register new device
    device_id = db.register_device(user_id, hostname, f"Laptop ({os_info})")
    if device_id:
        return jsonify({"status": "success", "device_id": device_id})
    return jsonify({"status": "error", "message": "Failed to register device"}), 400

# Set stricter Content Security Policy headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://unpkg.com; style-src 'self' 'unsafe-inline' https://unpkg.com; img-src 'self' data: https://*.tile.openstreetmap.org; connect-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)