import random, json, uuid, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Cat:
    def __init__(self, name, config):
        self.id = str(uuid.uuid4())
        self.name = name
        self.config = config
        self.pos = {'x': random.randint(0, 100), 'y': random.randint(0, 100)}
        self.stats = {'energy': 100, 'hunger': 0, 'thirst': 0, 'social': 50}
        self.action = 'idle'

    def update(self):
        self.stats['energy'] = max(0, self.stats['energy'] - self.config.get('energy_drain', 1))
        self.stats['hunger'] = min(100, self.stats['hunger'] + self.config.get('hunger_gain', 0.5))
        self.stats['thirst'] = min(100, self.stats['thirst'] + self.config.get('thirst_gain', 0.8))
        
        if self.stats['hunger'] > 80: self.action = 'eating'
        elif self.stats['thirst'] > 80: self.action = 'drinking'
        elif self.stats['energy'] < 20: self.action = 'sleeping'
        else:
            self.action = 'walking'
            self.pos['x'] = max(0, min(100, self.pos['x'] + random.randint(-2, 2)))
            self.pos['y'] = max(0, min(100, self.pos['y'] + random.randint(-2, 2)))

class Society:
    def __init__(self):
        self.config = {'energy_drain': 1, 'hunger_gain': 0.5, 'thirst_gain': 0.8}
        self.cats = [Cat(f'Cat-{i}', self.config) for i in range(10)]
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
            <div id="ui" style="position:absolute; padding:10px;">
                <h1>Cat Society Pro</h1>
                Energy Drain: <input type="range" id="ed" min="0" max="5" step="0.1" value="1">
                Hunger Gain: <input type="range" id="hg" min="0" max="5" step="0.1" value="0.5">
            </div>
            <script>
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer();
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);
                camera.position.z = 150;
                const cats = {};
                async function update() {
                    const res = await fetch('/api');
                    const data = await res.json();
                    data.cats.forEach(c => {
                        if(!cats[c.name]) {
                            const mesh = new THREE.Mesh(new THREE.BoxGeometry(5,5,5), new THREE.MeshBasicMaterial({color: Math.random()*0xffffff}));
                            scene.add(mesh);
                            cats[c.name] = mesh;
                        }
                        cats[c.name].position.x = c.pos.x - 50;
                        cats[c.name].position.y = c.pos.y - 50;
                    });
                }
                function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
                setInterval(update, 500); animate();
            </script></body></html>
            """)
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(society.get_data()).encode())

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8080), Server).serve_forever()
