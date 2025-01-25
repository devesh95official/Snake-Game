import pygame
from config import CELL_SIZE, GRID_SIZE

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [pygame.Vector2(GRID_SIZE//2 * CELL_SIZE, GRID_SIZE//2 * CELL_SIZE)]
        self.direction = pygame.Vector2(CELL_SIZE, 0)
        self.new_direction = pygame.Vector2(CELL_SIZE, 0)
        self.grow = False

    def update(self):
        if self.new_direction + self.direction != (0, 0):
            self.direction = self.new_direction
        
        new_head = self.body[-1] + self.direction
        # Screen wrapping
        new_head.x = new_head.x % (GRID_SIZE * CELL_SIZE)
        new_head.y = new_head.y % (GRID_SIZE * CELL_SIZE)
        
        self.body.append(new_head)
        
        if not self.grow:
            self.body.pop(0)
        self.grow = False

    def change_direction(self, new_dir):
        self.new_direction = new_dir

    def check_collision(self):
        head = self.body[-1]
        # Only check self-collision (walls removed)
        return len(self.body) != len(set((segment.x, segment.y) for segment in self.body))