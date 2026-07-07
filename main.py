import random
import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Cat:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.pos = {'x': random.randint(0, 100), 'y': random.randint(0, 100)}
        self.stats = {'energy': 100, 'hunger': 0, 'thirst': 0, 'social': 50}
        self.action = 'idle'

    def update(self):
        self.stats['energy'] = max(0, self.stats['energy'] - 1)
        self.stats['hunger'] = min(100, self.stats['hunger'] + 0.5)
        self.stats['thirst'] = min(100, self.stats['thirst'] + 0.8)
        
        if self.stats['hunger'] > 80: self.action = 'eating'
        elif self.stats['thirst'] > 80: self.action = 'drinking'
        elif self.stats['energy'] < 20: self.action = 'sleeping'
        else:
            self.action = 'walking'
            self.pos['x'] += random.randint(-2, 2)
            self.pos['y'] += random.randint(-2, 2)

class CatSociety:
    def __init__(self, num):
        self.cats = [Cat(f'Cat-{i}') for i in range(num)]
    def get_data(self):
        for c in self.cats: c.update()
        return [{'name': c.name, 'pos': c.pos, 'stats': c.stats, 'action': c.action} for c in self.cats]

society = CatSociety(10)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html><head><script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
            <body style="margin:0; background:#111;">
            <div id="ui" style="position:absolute; color:white; padding:10px;"><h1>Cat Society 3D</h1></div>
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
                    data.forEach(c => {
                        if(!cats[c.name]) {
                            const geo = new THREE.BoxGeometry(5,5,5);
                            const mat = new THREE.MeshBasicMaterial({color: Math.random()*0xffffff});
                            const mesh = new THREE.Mesh(geo, mat);
                            scene.add(mesh);
                            cats[c.name] = mesh;
                        }
                        cats[c.name].position.x = c.pos.x - 50;
                        cats[c.name].position.y = c.pos.y - 50;
                    });
                }
                function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
                setInterval(update, 500);
                animate();
            </script></body></html>
            """)
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(society.get_data()).encode())

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8080), Server).serve_forever()
