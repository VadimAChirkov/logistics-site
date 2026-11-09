#!/usr/bin/env python3
"""Лёгкий сервер сайта: статика + счётчик посещений + форма связи (email)."""
import os, json, re, smtplib, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from email.mime.text import MIMEText

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTER_FILE = os.path.join(SITE_DIR, 'visits.txt')
EMAIL_TO = "vchirkoff2@gmail.com"
EMAIL_FROM = "vchirkoff2@gmail.com"

_lock = threading.Lock()

def get_app_password():
    try:
        with open(os.path.expanduser("~/.bashrc")) as f:
            for line in f:
                if "GMAIL_APP_PASSWORD" in line and "export" in line:
                    m = re.search(r"GMAIL_APP_PASSWORD\s*=\s*['\"]?([^'\"]+)['\"]?", line)
                    if m:
                        return m.group(1).strip()
    except Exception:
        pass
    return None

def read_counter():
    try:
        with open(COUNTER_FILE) as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0

def increment_counter():
    with _lock:
        n = read_counter() + 1
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(n))
        return n

class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path):
        ext = os.path.splitext(path)[1].lower()
        ctype = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.svg': 'image/svg+xml',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
        }.get(ext, 'application/octet-stream')
        with open(path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/visit':
            self._json({'count': increment_counter()})
            return
        if path == '/api/counter':
            self._json({'count': read_counter()})
            return
        if path in ('/', ''):
            path = '/index.html'
        file_path = os.path.normpath(os.path.join(SITE_DIR, path.lstrip('/')))
        if not file_path.startswith(SITE_DIR) or not os.path.isfile(file_path):
            self.send_error(404)
            return
        self._file(file_path)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/contact':
            try:
                length = int(self.headers.get('Content-Length', 0))
                data = json.loads(self.rfile.read(length) or b'{}')
            except Exception:
                data = {}
            name = (data.get('name') or '').strip()
            message = (data.get('message') or '').strip()
            if not message:
                self._json({'ok': False, 'error': 'Сообщение пустое'}, 400)
                return
            ok, err = send_contact_email(name, message)
            if ok:
                self._json({'ok': True})
            else:
                self._json({'ok': False, 'error': err}, 500)
            return
        self.send_error(404)

    def log_message(self, *a):
        pass

def send_contact_email(name, message):
    pw = get_app_password()
    if not pw:
        return False, "Пароль приложения Gmail не найден"
    subject = "Сообщение с сайта: {}".format(name or "без имени")
    text = "Имя: {}\n\nСообщение:\n{}".format(name or "не указано", message)
    m = MIMEText(text, 'plain', 'utf-8')
    m['Subject'] = subject
    m['From'] = EMAIL_FROM
    m['To'] = EMAIL_TO
    try:
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        s.login(EMAIL_FROM, pw)
        s.send_message(m)
        s.quit()
        return True, None
    except Exception as e:
        return False, str(e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Сервер сайта запущен на http://127.0.0.1:{port}")
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()
