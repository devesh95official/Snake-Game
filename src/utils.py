import pygame
import json
from config import COLORS

def draw_text(surface, text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def load_highscore():
    try:
        with open('highscore.json', 'r') as f:
            return json.load(f).get('highscore', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_highscore(score):
    with open('highscore.json', 'w') as f:
        json.dump({'highscore': max(0, min(score, 9999))}, f)  # Cap between 0-9999

class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.base_color = COLORS['button']
        self.hover_color = COLORS['button_hover']
        self.current_color = self.base_color
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=5)
        draw_text(surface, self.text, self.font, COLORS['text'], 
                self.rect.centerx, self.rect.centery)
        
    def check_hover(self, mouse_pos):
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)