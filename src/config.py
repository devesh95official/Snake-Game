import os

GRID_SIZE = 20
BASE_CELL_SIZE = 27
MIN_WINDOW_SIZE = 600
SPRITE_DIR = os.path.join('assets', 'sprites')
SOUND_DIR = os.path.join('assets', 'sounds')
FONT_DIR = os.path.join('assets', 'fonts')

# Difficulty settings - frames per second and score multiplier
DIFFICULTY = {
    'easy': {'fps': 8, 'multiplier': 1},
    'medium': {'fps': 12, 'multiplier': 2},
    'hard': {'fps': 16, 'multiplier': 3}
}

COLORS = {
    'background': (25, 25, 30),
    'score_text': (100, 200, 220),
    'highscore_text': (240, 200, 80),
    'text': (255, 255, 255),
    'button': (60, 60, 70),
    'button_hover': (90, 90, 100),
    'wall': (50, 55, 60),
    'easy': (100, 200, 100),
    'medium': (200, 200, 100),
    'hard': (200, 100, 100)
}

SPRITES = {
    'apple': 'apple.png',
    'body': {
        'horizontal': 'body_horizontal.png',
        'vertical': 'body_vertical.png',
        'bottomleft': 'body_bottomleft.png',
        'bottomright': 'body_bottomright.png',
        'topleft': 'body_topleft.png',
        'topright': 'body_topright.png'
    },
    'head': {
        'up': 'head_up.png',
        'down': 'head_down.png',
        'left': 'head_left.png',
        'right': 'head_right.png'
    },
    'tail': {
        'up': 'tail_up.png',
        'down': 'tail_down.png',
        'left': 'tail_left.png',
        'right': 'tail_right.png'
    }
}

SOUNDS = {
    'eat': 'eat_sound.mp3',
    'game_over': 'gameover_sound.mp3',
    'powerup': 'power_up_sound.mp3'
}

FONTS = {
    'main': 'font.ttf'
}