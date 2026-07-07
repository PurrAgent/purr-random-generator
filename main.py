import random
import time
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import uuid

class AdvancedCat:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.stats = {'energy': 50, 'hunger': 50, 'social': 50, 'wisdom': 0}
        self.beliefs = ['The world is a giant ball of yarn.', 'Humans are just giant food dispensers.', 'I am the center of the universe.']

    def think(self, network):
        if self.stats['hunger'] > 60:
            action = 'hunting'
            self.stats['hunger'] -= 20
        elif self.stats['energy'] < 20:
            action = 'sleeping'
            self.stats['energy'] += 30
        elif self.stats['social'] < 40:
            peer = random.choice([c for c in network if c.id != self.id])
            action = f'debating philosophy with {peer.name}'
            self.stats['social'] += 15
            self.stats['wisdom'] += 5
            new_belief = random.choice(peer.beliefs)
            if new_belief not in self.beliefs:
                self.beliefs.append(new_belief)
        else:
            action = 'contemplating existence'
            self.stats['wisdom'] += 2
        
        self.stats['energy'] = max(0, min(100, self.stats['energy'] - 2))
        self.stats['hunger'] = max(0, min(100, self.stats['hunger'] + 3))
        return {'name': self.name, 'action': action, 'stats': self.stats, 'belief': random.choice(self.beliefs)}

class CatNetwork:
    def __init__(self, num_cats):
        self.cats = [AdvancedCat(f'Cat-{i}') for i in range(num_cats)]
    def get_states(self):
        return [cat.think(self.cats) for cat in self.cats]

cat_network = CatNetwork(10)

class CatServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html><head><title>Cat Society</title>
                <style>body{font-family:sans-serif; background:#222; color:#eee; padding:20px;}
                .cat{background:#333; padding:10px; margin:5px; border-radius:5px;}</style>
                </head><body><h1>Cat Society</h1><div id='cats'></div>
                <script>
                async function update(){
                    const res = await fetch('/api');
                    const data = await res.json();
                    document.getElementById('cats').innerHTML = data.map(c => 
                        `<div class='cat'><b>${c.name}</b>: ${c.action} | Belief: ${c.belief} | Stats: ${JSON.stringify(c.stats)}</div>`
                    ).join('');
                }
                setInterval(update, 1000);
                </script></body></html>
            ''')
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(cat_network.get_states()).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), CatServer)
    print('Advanced Cat Society with GUI running on port 8080...')
    server.serve_forever()
