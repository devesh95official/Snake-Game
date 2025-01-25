import random
import pygame
from config import GRID_SIZE, CELL_SIZE

class Food:
    def __init__(self):
        self.position = pygame.Vector2()
        self.randomize_position()

    def randomize_position(self):
        self.position.x = random.randint(0, GRID_SIZE-1) * CELL_SIZE
        self.position.y = random.randint(0, GRID_SIZE-1) * CELL_SIZE