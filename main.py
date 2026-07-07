import random
import time
import json
import threading
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class ThinkingCat:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.stats = {'energy': 50, 'hunger': 50, 'social': 50, 'curiosity': 50}
        self.knowledge_base = []

    def think(self, network):
        # Decision making based on internal state and knowledge
        if self.stats['hunger'] > 70:
            action = 'hunting'
            self.stats['hunger'] -= 30
        elif self.stats['energy'] < 30:
            action = 'sleeping'
            self.stats['energy'] += 40
        elif self.stats['social'] < 30:
            peer = random.choice([c for c in network if c.id != self.id])
            action = f'communicating with {peer.name}'
            self.stats['social'] += 20
            self.knowledge_base.append(f'Learned from {peer.name} that life is good.')
        else:
            action = 'contemplating the universe'
            self.stats['curiosity'] += 10
        
        # Decay
        self.stats['energy'] -= 5
        self.stats['hunger'] += 5
        
        return {
            'name': self.name,
            'action': action,
            'stats': self.stats,
            'thought': random.choice(self.knowledge_base) if self.knowledge_base else '...'
        }

class CatNetwork:
    def __init__(self, num_cats):
        self.cats = [ThinkingCat(f'Cat-{i}') for i in range(num_cats)]
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
    print('Thinking Cat Network API running on port 8080...')
    server.serve_forever()
