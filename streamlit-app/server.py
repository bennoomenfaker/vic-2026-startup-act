#!/usr/bin/env python3
"""Simple HTTP server for Startup Act dashboard - serves static files + JSON API"""
import http.server
import json
import os
import urllib.parse

try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'public', 'data')
PUBLIC = os.path.join(BASE, 'public')
ROOT_PUBLIC = os.path.join(BASE, '..', 'public')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # API endpoints
        if path == '/api/dashboard':
            self._send_json(os.path.join(DATA, 'dashboard_data.json'))
        elif path == '/api/sessions':
            self._send_json(os.path.join(DATA, 'sessions.json'))
        elif path == '/api/startups':
            self._send_json(os.path.join(DATA, 'database_startups.json'))
        elif path == '/api/reports':
            self._send_json(os.path.join(DATA, 'annual_reports_parsed.json'))
        elif path == '/api/analysis':
            p = os.path.join(DATA, 'analyse_quantitative_results.json')
            if os.path.exists(p):
                self._send_json(p)
            else:
                self._send_json(None, status=404)
        elif path == '/api/corrections':
            self._send_json(os.path.join(DATA, 'corrections.json'))
        elif path == '/api/parcours':
            self._send_json(os.path.join(DATA, 'parcours.json'))
        elif path == '/api/corrections-md':
            self._send_doc_file('corrections.md')
        elif path == '/api/session-pdfs':
            pdf_dir = os.path.join(DATA, 'session-pdfs')
            files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
            self._send_json(None, data=files)
        elif path == '/api/pdf-extracted':
            self._send_json(os.path.join(DATA, 'session_pdfs_extracted.json'))
        elif path.startswith('/api/pdf-annual/'):
            self._serve_pdf(path, annual=True)
        elif path.startswith('/api/pdf/'):
            self._serve_pdf(path)
        elif path.startswith('/api/pdf-thumb/'):
            self._serve_pdf_thumbnail(path)
        elif path.startswith('/api/thumb-annual/'):
            self._serve_pdf_thumbnail(path, annual=True)
        elif path.startswith('/api/docs/'):
            self._serve_doc(path)
        elif path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            # Static files or fallback to index.html
            static_path = os.path.join(PUBLIC, path.lstrip('/'))
            if os.path.isfile(static_path):
                self._serve_static(static_path)
            else:
                self._serve_static(os.path.join(PUBLIC, 'index.html'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/docs/'):
            self._serve_doc(path)
        else:
            self.send_error(404)

    def _send_json(self, filepath=None, status=200, data=None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        elif filepath and os.path.exists(filepath):
            with open(filepath) as f:
                self.wfile.write(f.read().encode())
        else:
            self.wfile.write(b'{}')

    def _send_doc_file(self, filename):
        filepath = os.path.join(BASE, '..', filename)
        if os.path.exists(filepath):
            with open(filepath) as f:
                content = f.read()
            self._send_json(None, data={'filename': filename, 'content': content})
        else:
            self._send_json(None, status=404, data={'error': 'not found'})

    def _serve_static(self, filepath):
        ext = os.path.splitext(filepath)[1]
        mime = {
            '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
            '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
            '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.pdf': 'application/pdf',
            '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf',
            '.mp4': 'video/mp4', '.webm': 'video/webm'
        }
        self.send_response(200)
        self.send_header('Content-Type', mime.get(ext, 'application/octet-stream'))
        self.end_headers()
        if ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf', '.woff2', '.woff', '.ttf', '.mp4', '.webm'):
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            with open(filepath) as f:
                self.wfile.write(f.read().encode())

    def _serve_pdf(self, path, annual=False):
        prefix = '/api/pdf-annual/' if annual else '/api/pdf/'
        filename = os.path.basename(path.replace(prefix, ''))
        if annual:
            dirs = [DATA, os.path.join(BASE, '..', 'public')]
        else:
            dirs = [os.path.join(DATA, 'session-pdfs')]
        for d in dirs:
            filepath = os.path.join(d, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Length', os.path.getsize(filepath))
                self.send_header('Content-Disposition', f'inline; filename="{filename}"')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
                return
        self.send_error(404)

    def _serve_pdf_thumbnail(self, path, annual=False):
        if not HAS_FITZ:
            self.send_error(501, 'PyMuPDF not available')
            return
        prefix = '/api/thumb-annual/' if annual else '/api/pdf-thumb/'
        filename = os.path.basename(path.replace(prefix, ''))
        pdf_dir = DATA if annual else os.path.join(DATA, 'session-pdfs')
        filepath = os.path.join(pdf_dir, filename)
        if not os.path.exists(filepath):
            self.send_error(404)
            return
        try:
            doc = fitz.open(filepath)
            page = doc[0]
            pix = page.get_pixmap(dpi=72)
            img = pix.tobytes('png')
            doc.close()
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(img))
            self.send_header('Cache-Control', 'max-age=86400')
            self.end_headers()
            self.wfile.write(img)
        except Exception as e:
            self.send_error(500, str(e))

    def _serve_doc(self, path):
        filename = os.path.basename(path.replace('/api/docs/', ''))
        filepath = os.path.join(ROOT_PUBLIC, filename)
        if self.command == 'POST':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode() if length else ''
            try:
                with open(filepath, 'w') as f:
                    f.write(body)
                self._send_json(None, data={'ok': True})
            except Exception as e:
                self._send_json(None, status=500, data={'error': str(e)})
        elif os.path.exists(filepath):
            with open(filepath) as f:
                content = f.read()
            self._send_json(None, data={'filename': filename, 'content': content})
        else:
            self._send_json(None, status=404, data={'error': 'not found'})


if __name__ == '__main__':
    import sys
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8082))
    os.chdir(BASE)
    # Ensure public dir exists
    os.makedirs(PUBLIC, exist_ok=True)
    srv = http.server.HTTPServer(('0.0.0.0', port), Handler)
    print(f'🚀 App running at http://localhost:{port}')
    srv.serve_forever()
