import random
import pygame
from config import GRID_SIZE, CELL_SIZE

class Food:
    def __init__(self):
        self.position = pygame.Vector2()
        
    def randomize_position(self, snake_body):
        while True:
            self.position.x = random.randint(0, GRID_SIZE-1) * CELL_SIZE
            self.position.y = random.randint(0, GRID_SIZE-1) * CELL_SIZE
            if not any(segment.x == self.position.x and 
                      segment.y == self.position.y for segment in snake_body):
                break