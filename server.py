"""Run with:  python3 server.py   (standard library only, no installs needed)"""
import http.server, socketserver, socket, os, urllib.request

PORT = 8000
WORDS_URL = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists("dictionary.txt"):
    print("Downloading ENABLE word list (one time)...")
    urllib.request.urlretrieve(WORDS_URL, "dictionary.txt")


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "localhost"
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


socketserver.ThreadingTCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as server:
    print(f"\nOn this computer: http://localhost:{PORT}")
    print(f"On your phone (same Wi-Fi): http://{lan_ip()}:{PORT}\n")
    server.serve_forever()
