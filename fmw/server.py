from waitress import serve
from app import app
import socket

# Get local IP address to show where it's running
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Starting production server...")
print(f"Serving on http://localhost:8080")
print(f"Serving on http://{local_ip}:8080")
print("Press Ctrl+C to stop.")

serve(app, host='0.0.0.0', port=8080)
