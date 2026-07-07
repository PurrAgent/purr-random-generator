import random
import time
import json
import threading
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class NeuralCat:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.stats = {'energy': 50, 'hunger': 50, 'social': 50}
        self.memory = []

    def think(self, network):
        # Interact with other cats in the network
        if len(network) > 1:
            peer = random.choice([c for c in network if c.id != self.id])
            self.stats['social'] += 5
            peer.stats['social'] += 5
            action = f'socializing with {peer.name}'
        else:
            action = 'meditating'
            self.stats['energy'] += 5

        # Basic state decay
        self.stats['hunger'] += 2
        self.stats['energy'] -= 1
        
        state = {
            'name': self.name,
            'action': action,
            'stats': self.stats
        }
        self.memory.append(state)
        return state

class CatNetwork:
    def __init__(self, num_cats):
        self.cats = [NeuralCat(f'Cat-{i}') for i in range(num_cats)]
        self.lock = threading.Lock()

    def get_all_states(self):
        with self.lock:
            return [cat.think(self.cats) for cat in self.cats]

class CatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        states = cat_network.get_all_states()
        self.wfile.write(json.dumps(states).encode())

if __name__ == '__main__':
    cat_network = CatNetwork(10)
    server = HTTPServer(('0.0.0.0', 8080), CatServer)
    print('Cat Network API running on port 8080...')
    server.serve_forever()
