import pygame
import os
from config import GRID_SIZE, BASE_CELL_SIZE, MIN_WINDOW_SIZE, COLORS, SPRITES, SPRITE_DIR, FONTS, FONT_DIR
from utils import Button, draw_text, load_highscores

class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.current_size = self.screen.get_size()
        pygame.display.set_caption("Snake Game")
        
        font_path = os.path.join(FONT_DIR, FONTS['main'])
        self.font = pygame.font.Font(font_path, 24)
        self.title_font = pygame.font.Font(font_path, 48)
        self.score_font = pygame.font.Font(font_path, 28)
        
        self.clock = pygame.time.Clock()
        self.cell_size = self.calculate_cell_size()
        self.game_width = GRID_SIZE * self.cell_size
        self.game_height = GRID_SIZE * self.cell_size
        self.background = pygame.Surface((MIN_WINDOW_SIZE, MIN_WINDOW_SIZE))
        self.background.fill(COLORS['wall'])
        
        self.sprites = self.load_sprites()

    def calculate_cell_size(self):
        return max(BASE_CELL_SIZE, min(self.current_size) // GRID_SIZE)

    def load_sprites(self):
        sprites = {
            'apple': pygame.image.load(os.path.join(SPRITE_DIR, SPRITES['apple'])).convert_alpha(),
            'body': {},
            'head': {},
            'tail': {}
        }

        for part, filename in SPRITES['body'].items():
            sprites['body'][part] = pygame.image.load(os.path.join(SPRITE_DIR, filename)).convert_alpha()

        for direction, filename in SPRITES['head'].items():
            sprites['head'][direction] = pygame.image.load(os.path.join(SPRITE_DIR, filename)).convert_alpha()

        for direction, filename in SPRITES['tail'].items():
            sprites['tail'][direction] = pygame.image.load(os.path.join(SPRITE_DIR, filename)).convert_alpha()

        return sprites

    def handle_resize(self, event):
        new_width = max(event.w, MIN_WINDOW_SIZE)
        new_height = max(event.h, MIN_WINDOW_SIZE)
        self.current_size = (new_width, new_height)
        self.screen = pygame.display.set_mode(self.current_size, pygame.RESIZABLE)
        self.cell_size = self.calculate_cell_size()
        self.game_width = GRID_SIZE * self.cell_size
        self.game_height = GRID_SIZE * self.cell_size

    def get_play_area(self):
        return (
            (self.current_size[0] - self.game_width) // 2,
            (self.current_size[1] - self.game_height) // 2
        )

    def draw_walls(self):
        self.screen.blit(pygame.transform.scale(self.background, self.current_size), (0, 0))
        x, y = self.get_play_area()
        
        border_rect = pygame.Rect(x - 12, y - 12, self.game_width + 24, self.game_height + 24)
        pygame.draw.rect(self.screen, COLORS['wall'], border_rect, border_radius=20)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = COLORS['grass1'] if (i + j) % 2 == 0 else COLORS['grass2']
                cell_rect = pygame.Rect(
                    x + i * self.cell_size,
                    y + j * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, cell_rect)
        
        inner_border = pygame.Rect(x, y, self.game_width, self.game_height)
        pygame.draw.rect(self.screen, COLORS['wall'], inner_border, border_radius=12, width=2)

    def draw_snake(self, snake):
        if len(snake.body) < 2:
            return
            
        x_offset, y_offset = self.get_play_area()
        
        if len(snake.body) >= 2:
            tail_dir = self.get_tail_direction(snake.body)
            self.draw_sprite(self.sprites['tail'][tail_dir], snake.body[-1], x_offset, y_offset)
        
        for i in range(1, len(snake.body)-1):
            prev = snake.body[i-1]
            curr = snake.body[i]
            next_seg = snake.body[i+1]
            body_sprite = self.get_body_sprite(prev, curr, next_seg)
            self.draw_sprite(body_sprite, curr, x_offset, y_offset)
        
        head_dir = self.get_head_direction(snake.body)
        self.draw_sprite(self.sprites['head'][head_dir], snake.body[0], x_offset, y_offset)

    def get_head_direction(self, body):
        dx = (body[0][0] - body[1][0]) % GRID_SIZE
        dy = (body[0][1] - body[1][1]) % GRID_SIZE
        
        if dx > 1: dx -= GRID_SIZE
        if dy > 1: dy -= GRID_SIZE
        
        if dx == 1: return 'right'
        if dx == -1: return 'left'
        if dy == 1: return 'down'
        return 'up'

    def get_tail_direction(self, body):
        if len(body) < 2:
            return 'up'
            
        dx = (body[-1][0] - body[-2][0]) % GRID_SIZE
        dy = (body[-1][1] - body[-2][1]) % GRID_SIZE
        
        if dx > 1: dx -= GRID_SIZE
        if dy > 1: dy -= GRID_SIZE
        
        if dx == 1: return 'right'
        if dx == -1: return 'left'
        if dy == 1: return 'down'
        return 'up'

    def get_body_sprite(self, prev, curr, next_seg):
        dx_prev = (curr[0] - prev[0]) % GRID_SIZE
        dy_prev = (curr[1] - prev[1]) % GRID_SIZE
        dx_next = (next_seg[0] - curr[0]) % GRID_SIZE
        dy_next = (next_seg[1] - curr[1]) % GRID_SIZE

        dx_prev = dx_prev if dx_prev <= 1 else dx_prev - GRID_SIZE
        dy_prev = dy_prev if dy_prev <= 1 else dy_prev - GRID_SIZE
        dx_next = dx_next if dx_next <= 1 else dx_next - GRID_SIZE
        dy_next = dy_next if dy_next <= 1 else dy_next - GRID_SIZE

        if dx_prev == dx_next and dy_prev == dy_next:
            return self.sprites['body']['horizontal' if dx_prev != 0 else 'vertical']
        
        if (dx_prev == 1 and dy_next == 1) or (dy_prev == -1 and dx_next == -1):
            return self.sprites['body']['bottomleft']
        if (dx_prev == -1 and dy_next == 1) or (dy_prev == -1 and dx_next == 1):
            return self.sprites['body']['bottomright']
        if (dx_prev == 1 and dy_next == -1) or (dy_prev == 1 and dx_next == -1):
            return self.sprites['body']['topleft']
        return self.sprites['body']['topright']

    def draw_sprite(self, sprite, grid_pos, x_offset, y_offset):
        scaled = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
        self.screen.blit(scaled, (
            x_offset + grid_pos[0] * self.cell_size,
            y_offset + grid_pos[1] * self.cell_size
        ))

    def draw_food(self, food_pos):
        x_offset, y_offset = self.get_play_area()
        self.draw_sprite(self.sprites['apple'], food_pos, x_offset, y_offset)

    def draw_score(self, score):
        x_offset, y_offset = self.get_play_area()
        draw_text(self.screen, f"SCORE: {score}", self.score_font,
                COLORS['score_text'], x_offset + 20, y_offset - 40, center=False)
        draw_text(self.screen, f"HIGHSCORE: {load_highscores()[0]}", self.score_font,
                COLORS['highscore_text'], x_offset + self.game_width - 20, y_offset - 40, center=False)

    def update_display(self, snake, food_pos, score, paused=False):
        self.draw_walls()
        self.draw_snake(snake)
        self.draw_food(food_pos)
        self.draw_score(score)
        
        if paused:
            draw_text(self.screen, "PAUSED", self.title_font, COLORS['text'],
                    self.current_size[0]//2, self.current_size[1]//2)
        
        pygame.display.flip()
        self.clock.tick(12)

    def create_button(self, y_pos, text, width=200, color=None, hover_color=None):
        return Button(
            (self.current_size[0] - width) // 2,
            y_pos,
            width,
            50,
            text,
            font_size=28,
            base_color=color or COLORS['button'],
            hover_color=hover_color or COLORS['button_hover']
        )

    def main_menu(self):
        gradient = pygame.Surface(self.current_size)
        for y in range(self.current_size[1]):
            blend = y / self.current_size[1]
            color = (
                int(COLORS['menu_gradient1'][0] * (1 - blend) + COLORS['menu_gradient2'][0] * blend),
                int(COLORS['menu_gradient1'][1] * (1 - blend) + COLORS['menu_gradient2'][1] * blend),
                int(COLORS['menu_gradient1'][2] * (1 - blend) + COLORS['menu_gradient2'][2] * blend)
            )
            pygame.draw.line(gradient, color, (0, y), (self.current_size[0], y))
        
        self.screen.blit(gradient, (0, 0))
        draw_text(self.screen, "SNAKE GAME", self.title_font, COLORS['menu_text'],
                self.current_size[0]//2, 80)
        
        buttons = [
            self.create_button(180, "Play", color=COLORS['accent1'], hover_color=COLORS['accent2']),
            self.create_button(260, "Highscores", color=COLORS['accent1'], hover_color=COLORS['accent2']),
            self.create_button(340, "Exit", color=COLORS['accent1'], hover_color=COLORS['accent2'])
        ]
        
        for btn in buttons:
            btn.draw(self.screen)
        
        pygame.display.flip()
        return buttons

    def game_over(self, score):
        self.screen.fill(COLORS['wall'])
        draw_text(self.screen, "GAME OVER", self.title_font, (200, 50, 50),
                self.current_size[0]//2, 100)
        draw_text(self.screen, f"FINAL SCORE: {score}", self.score_font,
                COLORS['text'], self.current_size[0]//2, 180)
        
        buttons = [
            self.create_button(240, "Play Again", 240),
            self.create_button(320, "Main Menu", 240)
        ]
        
        for btn in buttons:
            btn.draw(self.screen)
        
        pygame.display.flip()
        return buttons

    def display_highscores(self, highscores):
        self.screen.fill(COLORS['accent1'])
        for i in range(0, self.current_size[0], 40):
            pygame.draw.line(self.screen, COLORS['accent2'], (i, 0), (i, self.current_size[1]), 3)
        
        draw_text(self.screen, "TOP SCORES", self.title_font, COLORS['menu_text'],
                self.current_size[0]//2, 60)
        
        y_pos = 140
        for idx, score in enumerate(highscores[:10], 1):
            text_color = COLORS['score_highlight'] if idx == 1 else COLORS['menu_text']
            draw_text(self.screen, f"{idx:02}. {score:04}", self.score_font, text_color,
                    self.current_size[0]//2, y_pos)
            y_pos += 40
        
        back_btn = self.create_button(y_pos + 20, "Back", 150, 
                                    color=COLORS['accent2'], hover_color=COLORS['score_highlight'])
        back_btn.draw(self.screen)
        pygame.display.flip()
        
        return back_btn