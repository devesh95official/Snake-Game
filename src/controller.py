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
                if event.key == pygame.K_UP:
                    snake.change_direction(pygame.Vector2(0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(pygame.Vector2(0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(pygame.Vector2(-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(pygame.Vector2(CELL_SIZE, 0))
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused