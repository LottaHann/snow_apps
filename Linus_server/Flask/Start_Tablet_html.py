import http.server
import socketserver
import os
# Set the port number you want to use
port = 5500
# Set the path to the directory you want to serve
directory = r"D:/2024/tesis robot app/Tesis Robot/Linux/Tablet"
# Change to the specified directory
try:
    os.chdir(directory)
except FileNotFoundError:
    print(f"Error: Directory '{directory}' not found.")
    exit()

# Define the handler to use
handler = http.server.SimpleHTTPRequestHandler

# Create the server
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Serving on port {port} from directory {directory}...")
    # Start the server
    httpd.serve_forever()