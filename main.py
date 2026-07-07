import random, json, uuid, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler

class Cat:
    def __init__(self, name, config):
        self.id = str(uuid.uuid4())
        self.name = name
        self.config = config
        self.pos = {'x': random.randint(0, 100), 'y': random.randint(0, 100)}
        self.stats = {'energy': 100, 'hunger': 0, 'thirst': 0, 'mood': 50}
        self.action = 'idle'

    def update(self):
        self.stats['energy'] = max(0, min(100, self.stats['energy'] - self.config.get('energy_drain', 0.5)))
        self.stats['hunger'] = max(0, min(100, self.stats['hunger'] + self.config.get('hunger_gain', 0.2)))
        
        if self.stats['hunger'] > 80: self.action = 'eating'
        elif self.stats['energy'] < 20: self.action = 'sleeping'
        else:
            self.action = 'walking'
            self.pos['x'] = max(0, min(100, self.pos['x'] + random.randint(-2, 2)))
            self.pos['y'] = max(0, min(100, self.pos['y'] + random.randint(-2, 2)))

class Society:
    def __init__(self):
        self.config = {'energy_drain': 0.5, 'hunger_gain': 0.2, 'population': 10}
        self.cats = [Cat(f'Cat-{i}', self.config) for i in range(self.config['population'])]
    
    def update_config(self, new_config):
        self.config.update({k: float(v) for k, v in new_config.items()})

    def get_data(self):
        for c in self.cats: c.update()
        return {'cats': [{'name': c.name, 'pos': c.pos, 'stats': c.stats, 'action': c.action} for c in self.cats], 'config': self.config}

society = Society()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html><head><script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
            <body style="margin:0; background:#111; color:white;">
            <div id="ui" style="position:absolute; padding:10px; background:rgba(0,0,0,0.5);">
                <h1>Cat Society Optimized</h1>
                Energy Drain: <input type="range" id="ed" min="0" max="2" step="0.1" value="0.5" onchange="updateConfig()">
            </div>
            <script>
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({antialias: false});
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);
                camera.position.z = 100;
                const cats = {};
                async function updateConfig() {
                    await fetch('/config', {method: 'POST', body: JSON.stringify({energy_drain: document.getElementById('ed').value})});
                }
                async function update() {
                    const res = await fetch('/api');
                    const data = await res.json();
                    data.cats.forEach(c => {
                        if(!cats[c.name]) {
                            const mesh = new THREE.Mesh(new THREE.BoxGeometry(4,4,4), new THREE.MeshBasicMaterial({color: 0x00ff00}));
                            scene.add(mesh);
                            cats[c.name] = mesh;
                        }
                        cats[c.name].position.set(c.pos.x - 50, c.pos.y - 50, 0);
                    });
                }
                function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
                setInterval(update, 1000); animate();
            </script></body></html>
            """)
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(society.get_data()).encode())
    
    def do_POST(self):
        if self.path == '/config':
            content_length = int(self.headers['Content-Length'])
            society.update_config(json.loads(self.rfile.read(content_length)))
            self.send_response(200); self.end_headers()

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8080), Server).serve_forever()
