import pygame
from config import *
from utils import Button, draw_text

class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT + 40))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for x in range(0, GAME_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, GAME_HEIGHT))
        for y in range(0, GAME_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLORS['grid'], (0, y), (GAME_WIDTH, y))

    def draw_snake(self, snake):
        for segment in snake.body:
            pygame.draw.rect(self.screen, COLORS['snake'], 
                           (segment.x + 2, segment.y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 
                           border_radius=4)

    def draw_food(self, food):
        pygame.draw.circle(self.screen, COLORS['food'], 
                         (food.position.x + CELL_SIZE//2, food.position.y + CELL_SIZE//2),
                         CELL_SIZE//2 - 3)

    def draw_score(self, score):
        score_surface = self.font.render(f"Score: {score}", True, COLORS['text'])
        self.screen.blit(score_surface, (10, GAME_HEIGHT + 5))

    def update_display(self, snake, food, score):
        self.screen.fill(COLORS['background'])
        self.draw_grid()
        self.draw_snake(snake)
        self.draw_food(food)
        self.draw_score(score)
        pygame.display.flip()
        self.clock.tick(FPS)

    def main_menu(self, highscore):
        self.screen.fill(COLORS['background'])
        draw_text(self.screen, "SNAKE GAME", self.title_font, COLORS['text'], 
                GAME_WIDTH//2, 100)
        draw_text(self.screen, f"High Score: {highscore}", self.font, COLORS['text'], 
                GAME_WIDTH//2, 200)
        
        play_btn = Button(GAME_WIDTH//2 - 100, 300, 200, 50, "Play")
        exit_btn = Button(GAME_WIDTH//2 - 100, 400, 200, 50, "Exit")
        return play_btn, exit_btn

    def game_over(self, score):
        self.screen.fill(COLORS['background'])
        draw_text(self.screen, "Game Over!", self.title_font, COLORS['text'], 
                GAME_WIDTH//2, 100)
        draw_text(self.screen, f"Score: {score}", self.font, COLORS['text'], 
                GAME_WIDTH//2, 200)
        
        restart_btn = Button(GAME_WIDTH//2 - 100, 300, 200, 50, "Restart")
        menu_btn = Button(GAME_WIDTH//2 - 100, 400, 200, 50, "Main Menu")
        return restart_btn, menu_btn