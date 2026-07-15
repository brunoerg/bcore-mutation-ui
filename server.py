import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

    def send_head(self):
        # SPA fallback: deep links like /src/net_processing.cpp or /pull/35221/...
        # aren't real files, so serve index.html and let the client-side router
        # render the right view (mirrors 404.html on GitHub Pages).
        path = self.translate_path(self.path)
        if not os.path.exists(path) and not os.path.isdir(path):
            self.path = '/index.html'
        return super().send_head()

httpd = HTTPServer(('localhost', 8000), CORSRequestHandler)
print("Serving at port 8000")
httpd.serve_forever()
