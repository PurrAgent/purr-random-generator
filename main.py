import random
import time
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class AICatGenerator:
    def __init__(self):
        self.purrs = ['Meow!', 'Purrr...', 'Mrow?', 'Nya!', 'Hiss!', 'Prrrp!', 'Chirp!']
        self.energy = 50
        self.hunger = 50
        self.history = []
        self.current_state = {}

    def think(self):
        # AI-like decision making based on internal state
        if self.hunger > 70:
            action = 'looking for food'
            self.hunger -= 20
            self.energy -= 5
        elif self.energy < 30:
            action = 'taking a nap'
            self.energy += 30
            self.hunger += 5
        elif self.energy > 80:
            action = 'running around'
            self.energy -= 20
            self.hunger += 10
        else:
            action = 'purring'
            self.energy -= 2
            self.hunger += 2
        
        self.current_state = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'sound': random.choice(self.purrs),
            'stats': {'energy': self.energy, 'hunger': self.hunger}
        }
        self.history.append(self.current_state)

    def run_simulation_loop(self):
        while True:
            self.think()
            time.sleep(2)

class CatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(cat_gen.current_state)
        self.wfile.write(response.encode())

if __name__ == '__main__':
    cat_gen = AICatGenerator()
    
    # Start simulation in background
    sim_thread = threading.Thread(target=cat_gen.run_simulation_loop, daemon=True)
    sim_thread.start()
    
    # Start web server
    server = HTTPServer(('0.0.0.0', 8080), CatServer)
    print('AI Cat API running on port 8080...')
    server.serve_forever()
