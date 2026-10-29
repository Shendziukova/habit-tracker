import os, webbrowser, threading, http.server, socketserver, time

PORT = 8765
DIR = os.path.dirname(os.path.abspath(__file__))

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)

def main():
    httpd = socketserver.TCPServer(("", PORT), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
