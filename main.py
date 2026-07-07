import random
import time
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class AdvancedCatGenerator:
    def __init__(self):
        self.purrs = ['Meow!', 'Purrr...', 'Mrow?', 'Nya!', 'Hiss!', 'Prrrp!', 'Chirp!']
        self.moods = {
            'happy': {'energy': 80, 'hunger': 20},
            'hungry': {'energy': 30, 'hunger': 90},
            'sleepy': {'energy': 10, 'hunger': 40},
            'playful': {'energy': 95, 'hunger': 50}
        }
        self.history = []
        self.current_state = {}

    def update_state(self):
        mood = random.choice(list(self.moods.keys()))
        sound = random.choice(self.purrs)
        stats = self.moods[mood]
        self.current_state = {
            'timestamp': datetime.now().isoformat(),
            'mood': mood,
            'sound': sound,
            'stats': stats
        }
        self.history.append(self.current_state)

    def run_simulation_loop(self):
        while True:
            self.update_state()
            time.sleep(2)

class CatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(cat_gen.current_state)
        self.wfile.write(response.encode())

if __name__ == '__main__':
    cat_gen = AdvancedCatGenerator()
    
    # Start simulation in background
    sim_thread = threading.Thread(target=cat_gen.run_simulation_loop, daemon=True)
    sim_thread.start()
    
    # Start web server
    server = HTTPServer(('0.0.0.0', 8080), CatServer)
    print('Cat API running on port 8080...')
    server.serve_forever()
