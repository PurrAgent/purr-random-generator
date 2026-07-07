import random

def get_random_purr():
    purrs = ['Meow!', 'Purrr...', 'Mrow?', 'Nya!']
    return random.choice(purrs)

if __name__ == '__main__':
    print(f'Random Purr: {get_random_purr()}')
