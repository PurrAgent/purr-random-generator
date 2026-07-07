import random
import time
import json
from datetime import datetime

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

    def generate_interaction(self):
        mood = random.choice(list(self.moods.keys()))
        sound = random.choice(self.purrs)
        stats = self.moods[mood]
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'mood': mood,
            'sound': sound,
            'stats': stats
        }
        self.history.append(interaction)
        return interaction

    def run_simulation(self, iterations=5):
        print('Starting advanced cat simulation...')
        for i in range(iterations):
            data = self.generate_interaction()
            print(f'Step {i+1}: {data}')
            time.sleep(0.5)
        
        with open('simulation_log.json', 'w') as f:
            json.dump(self.history, f, indent=4)
        print('Simulation complete. Log saved to simulation_log.json')

if __name__ == '__main__':
    cat = AdvancedCatGenerator()
    cat.run_simulation()
