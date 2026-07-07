import random
import time

class CatGenerator:
    def __init__(self):
        self.purrs = ['Meow!', 'Purrr...', 'Mrow?', 'Nya!', 'Hiss!', 'Prrrp!']
        self.moods = ['happy', 'hungry', 'sleepy', 'playful']

    def generate_interaction(self):
        mood = random.choice(self.moods)
        sound = random.choice(self.purrs)
        return f'The cat is feeling {mood} and says: {sound}'

    def run_simulation(self, iterations=5):
        print('Starting cat simulation...')
        for i in range(iterations):
            print(f'Step {i+1}: {self.generate_interaction()}')
            time.sleep(1)
        print('Simulation complete.')

if __name__ == '__main__':
    cat = CatGenerator()
    cat.run_simulation()
