import pygame
import json
from config import COLORS, FONTS, FONT_DIR
import os

def draw_text(surface, text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def load_highscores():
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f).get('scores', [])
            return sorted(scores, reverse=True)[:10]
    except (FileNotFoundError, json.JSONDecodeError):
        return [0] * 10

def save_highscore(score):
    scores = load_highscores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:10]
    with open('highscores.json', 'w') as f:
        json.dump({'scores': scores}, f)

class Button:
    def __init__(self, x, y, width, height, text, font_size=28):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        font_path = os.path.join(FONT_DIR, FONTS['main'])
        self.font = pygame.font.Font(font_path, font_size)
        self.base_color = COLORS['button']
        self.hover_color = COLORS['button_hover']
        self.current_color = self.base_color
        self.hover_frame_count = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=8)
        draw_text(surface, self.text, self.font, COLORS['text'], 
                self.rect.centerx, self.rect.centery)

    def check_hover(self, mouse_pos):
        was_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if was_hovered else self.base_color
        self.hover_frame_count = 5 if was_hovered else max(0, self.hover_frame_count - 1)
        return was_hovered
        
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)