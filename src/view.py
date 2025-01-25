import pygame
from config import GRID_SIZE, BASE_CELL_SIZE, MIN_WINDOW_SIZE, COLORS
from utils import Button, draw_text, load_highscores

class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.current_size = self.screen.get_size()
        pygame.display.set_caption("Snake Game")
        
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        
        self.cell_size = self.calculate_cell_size()
        self.game_width = GRID_SIZE * self.cell_size
        self.game_height = GRID_SIZE * self.cell_size

    def calculate_cell_size(self):
        return max(BASE_CELL_SIZE, min(self.current_size) // GRID_SIZE)

    def handle_resize(self, event):
        new_width = max(event.w, MIN_WINDOW_SIZE)
        new_height = max(event.h, MIN_WINDOW_SIZE)
        self.current_size = (new_width, new_height)
        self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
        self.cell_size = self.calculate_cell_size()
        self.game_width = GRID_SIZE * self.cell_size
        self.game_height = GRID_SIZE * self.cell_size

    def scale_position(self, grid_pos):
        x_offset = (self.current_size[0] - self.game_width) // 2
        y_offset = (self.current_size[1] - self.game_height) // 2
        return pygame.Vector2(
            x_offset + grid_pos[0] * self.cell_size,
            y_offset + grid_pos[1] * self.cell_size
        )

    def draw_snake(self, snake):
        for segment in snake.body:
            pos = self.scale_position(segment)
            pygame.draw.rect(self.screen, COLORS['snake'], 
                           (pos.x, pos.y, self.cell_size, self.cell_size), 
                           border_radius=4)

    def draw_food(self, food_pos):
        pos = self.scale_position(food_pos)
        pygame.draw.circle(self.screen, COLORS['food'], 
                         (pos.x + self.cell_size//2, pos.y + self.cell_size//2),
                         self.cell_size//2 - 3)

    def draw_score(self, score):
        draw_text(self.screen, f"Score: {score}", self.font, COLORS['text'], 
                20, 10, center=False)
        draw_text(self.screen, f"High Score: {load_highscores()[0]}", self.font, 
                COLORS['text'], self.current_size[0] - 20, 10, center=False)

    def update_display(self, snake, food_pos, score, paused=False):
        self.screen.fill(COLORS['background'])
        self.draw_snake(snake)
        self.draw_food(food_pos)
        self.draw_score(score)
        
        if paused:
            draw_text(self.screen, "PAUSED", self.title_font, COLORS['text'], 
                    self.current_size[0]//2, self.current_size[1]//2)
        
        pygame.display.flip()
        self.clock.tick(12)

    def create_button(self, y_pos, text, width=200):
        return Button(
            (self.current_size[0] - width) // 2,
            y_pos,
            width,
            50,
            text
        )

    def main_menu(self):
        self.screen.fill(COLORS['background'])
        draw_text(self.screen, "SNAKE GAME", self.title_font, COLORS['text'], 
                self.current_size[0]//2, 50)
        
        buttons = [
            self.create_button(150, "Play"),
            self.create_button(220, "Highscores"),
            self.create_button(290, "Exit")
        ]
        
        for btn in buttons:
            btn.draw(self.screen)
        
        pygame.display.flip()
        return buttons

    def game_over(self, score):
        self.screen.fill(COLORS['background'])
        draw_text(self.screen, "GAME OVER", self.title_font, (255, 50, 50), 
                self.current_size[0]//2, 50)
        draw_text(self.screen, f"Score: {score}", self.font, COLORS['text'], 
                self.current_size[0]//2, 130)
        
        buttons = [
            self.create_button(180, "Play Again", 240),
            self.create_button(250, "Main Menu", 240)
        ]
        
        for btn in buttons:
            btn.draw(self.screen)
        
        pygame.display.flip()
        return buttons

    def display_highscores(self, highscores):
        self.screen.fill(COLORS['background'])
        draw_text(self.screen, "TOP SCORES", self.title_font, COLORS['text'], 
                self.current_size[0]//2, 50)
        
        y_pos = 120
        for idx, score in enumerate(highscores[:10], 1):
            text_color = (255, 215, 0) if idx == 1 else COLORS['text']
            draw_text(self.screen, f"{idx}. {score:04d}", self.score_font, text_color,
                    self.current_size[0]//2, y_pos)
            y_pos += 40
        
        back_btn = self.create_button(y_pos + 20, "Back", 150)
        back_btn.draw(self.screen)
        pygame.display.flip()
        
        return back_btn