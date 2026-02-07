from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # This response does NOT contain "fully booked" or "at capacity"
        self.wfile.write(b"<html><body><h1>Reservations Available!</h1><p>Pick your slot now.</p></body></html>")

def run_mock_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MockHandler)
    print("Test server running on http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    # Start server in a background thread
    daemon = threading.Thread(target=run_mock_server, daemon=True)
    daemon.start()
    
    # Wait a second for it to start
    time.sleep(1)
    print("Simulating available slot scenario...")
    
    # We will now run a modified version of the monitor check logic against localhost
    import monitor
    
    # Temporarily point monitor to localhost
    original_url = monitor.URL
    monitor.URL = "http://localhost:8000"
    
    available, msg = monitor.check_availability()
    print(f"Monitor detected: {'AVAILABLE' if available else 'UNAVAILABLE'}")
    print(f"Message: {msg}")
    
    if available:
        print("Sending TEST notification to Telegram...")
        monitor.notify(f"🚨 TEST ALERT: Rembayung available slots detected! (Simulation)\n\nBook here: {monitor.URL}")
    
    # Keep server alive for a bit
    time.sleep(2)
    print("Test complete.")
