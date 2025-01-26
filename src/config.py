import os

GRID_SIZE = 20
BASE_CELL_SIZE = 27
MIN_WINDOW_SIZE = 600
SPRITE_DIR = os.path.join('assets', 'sprites')
SOUND_DIR = os.path.join('assets', 'sounds')
FONT_DIR = os.path.join('assets', 'fonts')

COLORS = {
    'background': (25, 25, 30),
    'score_text': (100, 200, 220),
    'highscore_text': (240, 200, 80),
    'text': (255, 255, 255),
    'button': (60, 60, 70),
    'button_hover': (90, 90, 100),
    'wall': (50, 55, 60),
    'grass1': (159, 197, 74),
    'grass2': (131, 177, 73),
    'menu_gradient1': (255, 179, 71),
    'menu_gradient2': (238, 96, 156),
    'accent1': (74, 144, 217),
    'accent2': (255, 221, 89),
    'score_highlight': (255, 105, 97),
    'menu_text': (255, 255, 255)
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
    'game_over': 'gameover_sound.mp3'
}

FONTS = {
    'main': 'font.ttf'
}