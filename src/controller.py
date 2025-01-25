import pygame
from config import CELL_SIZE

class GameController:
    def __init__(self):
        self.quit = False
        self.paused = False

    def handle_input(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    snake.change_direction(pygame.Vector2(0, -CELL_SIZE))
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    snake.change_direction(pygame.Vector2(0, CELL_SIZE))
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    snake.change_direction(pygame.Vector2(-CELL_SIZE, 0))
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    snake.change_direction(pygame.Vector2(CELL_SIZE, 0))
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused