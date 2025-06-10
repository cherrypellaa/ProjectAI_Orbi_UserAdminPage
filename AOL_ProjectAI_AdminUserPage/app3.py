from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import subprocess, json, multiprocessing, pyttsx3, os, requests, sys
from pytz import timezone
import pytz

app = Flask(__name__)
detection_mode = multiprocessing.Value('b', False)

app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orbi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    logs = db.relationship('ActivityLog', back_populates='user')
    role = db.Column(db.String(50), nullable=False, default='user')

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(255))
    location = db.Column(db.String(255))  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='logs')

    @property
    def local_time(self):
        if self.timestamp is None:
            return None
        utc = pytz.UTC
        local_tz = timezone('Asia/Jakarta')
        return self.timestamp.replace(tzinfo=utc).astimezone(local_tz)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add_all([
            User(username='admin', password=generate_password_hash('admin'), role='admin'),
            User(username='user', password=generate_password_hash('user'), role='user')
        ])
        db.session.commit()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

def speak_text(text):
    p = multiprocessing.Process(target=speak, args=(text,))
    p.start()

def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        city = data.get('city', '')
        region = data.get('region', '')
        country = data.get('country', '')
        return f"{city}, {region}, {country}" if city or region or country else ip
    except Exception:
        return ip

def reverse_geocode(lat, lon):
    try:
        url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1'
        headers = {'User-Agent': 'orbi-app'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', f"{lat}, {lon}")
        return f"{lat}, {lon}"
    except Exception as e:
        print(f"Reverse geocoding error: {e}")
        return f"{lat}, {lon}"

def log_action(user_id, action):
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        location = session.get('user_location') or get_geolocation(ip)
        if user_id:
            log = ActivityLog(user_id=user_id, action=action, location=location)
            db.session.add(log)
            db.session.commit()
    except Exception as e:
        print(f"Log error: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for(session['role']))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'user')
        if not username or not password:
            return render_template('register.html', error="Username and password required.")
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists.")
        hashed_pw = generate_password_hash(password)
        db.session.add(User(username=username, password=hashed_pw, role=role))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/user')
def user():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template('user.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    username = request.args.get('username', '').strip()
    
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            logs = ActivityLog.query.filter_by(user_id=user.id).order_by(ActivityLog.timestamp.desc()).all()
            latest = logs[0] if logs else None
            return render_template('admin.html', logs=logs, latest=latest, searched_user=username)
        else:
            return render_template('admin.html', logs=[], latest=None, error="User tidak ditemukan.", searched_user=username)

    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(50).all()
    latest = logs[0] if logs else None

    return render_template('admin.html', logs=logs, latest=latest)

@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(result="Unauthorized"), 403

    data = request.json
    command = data.get('command', '').lower() if data.get('command') else ""
    response = ""

    if "hello" in command or "hey orbi" in command:
        response = "Hello! What can I help you with today?"
        speak_text(response)
        return jsonify({"result": response})

    if "detect object" in command:
        with detection_mode.get_lock():
            detection_mode.value = True
        response = "Object detection mode started."
        speak_text(response)
        return jsonify({"result": response})

    if "stop detecting object" in command:
        with detection_mode.get_lock():
            detection_mode.value = False
        response = "Object detection stopped."
        speak_text(response)
        return jsonify({"result": response})

    if "read text" in command:
        response = "Starting text reading."
        speak_text(response)
        try:
            subprocess.Popen(["python", "readtext.py"])  
        except Exception as e:
            response = f"Error starting text reader: {str(e)}"
        return jsonify({"result": response})

    if not command and not detection_mode.value:
        return jsonify({"result": ""})

    response = "Sorry, I didn't understand."
    log_action(user_id, command)
    return jsonify(result=response)

@app.route('/auto_detect')
def auto_detect():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(result="Unauthorized"), 403

    with detection_mode.get_lock():
        if not detection_mode.value:
            return jsonify({"result": "Detection is off."})

    try:
        result = subprocess.run(
            ["python", "detectobject2.py"],
        
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout_text = result.stdout.strip()
        stderr_text = result.stderr.strip()

        if stdout_text:
            try:
                detected = json.loads(stdout_text)
                response = f"Detected objects: {', '.join(detected)}" if detected else "No object detected."
            except json.JSONDecodeError:
                response = f"Raw Output: {stdout_text}"
        else:
            response = "No object detected."

        if stderr_text:
            response += f" (stderr: {stderr_text})"

    except subprocess.TimeoutExpired:
        response = "Detection timeout."
    except Exception as e:
        response = f"Detection error: {str(e)}"

    speak_text(response)
    log_action(user_id, response)
    return jsonify(result=response)

@app.route('/log_location', methods=['POST'])
def log_location():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is not None and longitude is not None:
        location_str = reverse_geocode(latitude, longitude)
        session['user_location'] = location_str
        log = ActivityLog(user_id=user_id, action="Location Update", location=location_str)
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Location logged'}), 200
    return jsonify({'message': 'Invalid data'}), 400

if __name__ == '__main__':
    multiprocessing.freeze_support()
    app.run(debug=True, port=5000)
