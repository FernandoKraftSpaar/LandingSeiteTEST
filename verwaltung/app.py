# Minimal administrative backend (Flask) with Azure SQL (SQLAlchemy) and placeholders para CRMs
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os, urllib.parse, requests, datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load config from environment
DATABASE_URL = os.environ.get('DATABASE_URL')  # example: "mssql+pyodbc://user:pass@server.database.windows.net:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server"
if not DATABASE_URL:
    # fallback local sqlite for dev
    DATABASE_URL = os.environ.get('SQLITE_URL', 'sqlite:///admin_dev.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='operator')

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class ClientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    source = db.Column(db.String(100))  # ex: hubspot, pipedrive
    active = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# --- Simple auth endpoints (tokenless, for demo only) ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error':'user exists'}), 400
    u = User(username=data.get('username'), email=data.get('email'),
             password_hash=generate_password_hash(data.get('password')), role=data.get('role','operator'))
    db.session.add(u); db.session.commit()
    return jsonify({'ok':True}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error':'invalid'}), 401
    # In production: return JWT or set secure session cookie
    return jsonify({'ok':True, 'user': {'username': user.username, 'role': user.role}})

# --- Admin APIs ---
@app.route('/api/users')
def list_users():
    users = User.query.all()
    return jsonify([{'username':u.username,'email':u.email,'role':u.role} for u in users])

@app.route('/api/overview')
def api_overview():
    # Aggregate local DB + CRMs
    total_local = ClientRecord.query.filter_by(active=True).count()
    crm_totals = {}
    # Attempt to call CRM integrations (these functions use env variables)
    try:
        hub_total = get_hubspot_active_count()
        crm_totals['hubspot'] = hub_total
    except Exception as e:
        crm_totals['hubspot'] = None
    try:
        pip_total = get_pipedrive_active_count()
        crm_totals['pipedrive'] = pip_total
    except Exception as e:
        crm_totals['pipedrive'] = None

    total_clients = total_local + sum(v or 0 for v in crm_totals.values())
    return jsonify({
        'totalClients': total_clients,
        'newLeads': 0,
        'alerts': 0,
        'crm': crm_totals
    })

# --- Placeholder CRM helpers ---
def get_hubspot_active_count():
    # Expect HUBSPOT_API_KEY or HUBSPOT_OAUTH_TOKEN in env
    api_key = os.environ.get('HUBSPOT_API_KEY')
    token = os.environ.get('HUBSPOT_OAUTH_TOKEN')
    headers = {}
    params = {'limit': 1}
    if token:
        headers['Authorization'] = f'Bearer {token}'
        url = 'https://api.hubapi.com/crm/v3/objects/contacts'
        r = requests.get(url, headers=headers, params=params, timeout=10)
    elif api_key:
        url = 'https://api.hubapi.com/contacts/v1/lists/all/contacts/all'
        r = requests.get(url, params={'hapikey': api_key, 'count': 1}, timeout=10)
    else:
        raise RuntimeError('No HubSpot credentials')
    if r.status_code != 200:
        raise RuntimeError('HubSpot request failed')
    # For demo we return a simple number; in production parse response and possibly paginated counts
    return 0  # adjust to parse actual result

def get_pipedrive_active_count():
    token = os.environ.get('PIPEDRIVE_API_TOKEN')
    if not token:
        raise RuntimeError('No Pipedrive token')
    url = f"https://api.pipedrive.com/v1/persons?api_token={token}&start=0&limit=1"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise RuntimeError('Pipedrive request failed')
    return 0

# --- Serve admin UI static file ---
@app.route('/admin')
def admin_ui():
    return send_from_directory('.', 'admin/index.html')

# --- Init DB route for dev only ---
@app.route('/admin/init-db')
def init_db():
    db.create_all()
    # create demo admin if not exists
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('adminpass'), role='admin')
        db.session.add(u); db.session.commit()
    return "initialized"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
