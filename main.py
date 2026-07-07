import random
import time
import json
import threading
import uuid
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import math

class NeuralCat:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.stats = {'energy': 50, 'hunger': 50, 'social': 50, 'curiosity': 50}
        self.weights = {k: random.uniform(0.5, 1.5) for k in self.stats}
        self.memory = []
        self.lock = threading.Lock()

    def _activation(self, x):
        return 1 / (1 + math.exp(-x))

    def think(self):
        with self.lock:
            # Neural-like decision process
            inputs = [self.stats[k] / 100 for k in self.stats]
            decision_score = sum(inputs[i] * list(self.weights.values())[i] for i in range(len(inputs)))
            
            if decision_score > 2.5:
                action = 'complex hunting'
                self.stats['hunger'] -= 20
                self.stats['energy'] -= 15
            elif decision_score > 1.5:
                action = 'socializing'
                self.stats['social'] += 15
                self.stats['energy'] -= 5
            else:
                action = 'meditating'
                self.stats['energy'] += 10
                self.stats['curiosity'] += 5

            # Normalize stats
            for k in self.stats:
                self.stats[k] = max(0, min(100, self.stats[k]))

            state = {
                'id': self.id,
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'stats': self.stats,
                'neural_score': round(decision_score, 2)
            }
            self.memory.append(state)
            return state

class CatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        state = cat_gen.think()
        self.wfile.write(json.dumps(state).encode())

if __name__ == '__main__':
    cat_gen = NeuralCat()
    server = HTTPServer(('0.0.0.0', 8080), CatServer)
    print('Neural AI Cat API running on port 8080...')
    server.serve_forever()
