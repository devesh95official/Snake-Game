import random

class Food:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.position = (0, 0)
        self.randomize_position([])

    def randomize_position(self, snake_body):
        while True:
            self.position = (
                random.randint(0, self.grid_size-1),
                random.randint(0, self.grid_size-1)
            )
            if self.position not in snake_body:
                break