import pygame
import os
import random
from src.config import GRID_SIZE, BASE_CELL_SIZE, MIN_WINDOW_SIZE, COLORS, SPRITES, SPRITE_DIR, FONTS, FONT_DIR, DIFFICULTY
from src.utils import Button, draw_text, load_highscores

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
        
        # Create gradient background
        self.create_gradient_background()
        
        self.sprites = self.load_sprites()

    def create_gradient_background(self):
        """Create a gradient background for better visual appearance"""
        self.gradient_bg = pygame.Surface(self.current_size)
        color1 = (20, 20, 35)  # Dark blue-purple
        color2 = (40, 40, 70)  # Lighter blue-purple
        
        for y in range(self.current_size[1]):
            # Calculate the ratio (0 to 1) based on y position
            ratio = y / self.current_size[1]
            # Create a gradient color
            r = color1[0] * (1 - ratio) + color2[0] * ratio
            g = color1[1] * (1 - ratio) + color2[1] * ratio
            b = color1[2] * (1 - ratio) + color2[2] * ratio
            # Draw a horizontal line with the calculated color
            pygame.draw.line(self.gradient_bg, (r, g, b), (0, y), (self.current_size[0], y))

    def calculate_cell_size(self):
        # Make sure the game area doesn't take up the entire screen
        # Leave room for UI elements
        max_game_width = self.current_size[0] * 0.8
        max_game_height = self.current_size[1] * 0.8
        
        return max(BASE_CELL_SIZE, min(max_game_width, max_game_height) // GRID_SIZE)

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
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        self.current_size = (new_width, new_height)
        self.cell_size = self.calculate_cell_size()
        self.game_width = GRID_SIZE * self.cell_size
        self.game_height = GRID_SIZE * self.cell_size
        
        # Recreate gradient background after resize
        self.create_gradient_background()

    def get_play_area(self):
        x_offset = (self.current_size[0] - self.game_width) // 2
        y_offset = (self.current_size[1] - self.game_height) // 2
        return x_offset, y_offset

    def draw_walls(self):
        self.screen.blit(pygame.transform.scale(self.background, self.current_size), (0, 0))
        x, y = self.get_play_area()
        
        border_rect = pygame.Rect(x - 12, y - 12, self.game_width + 24, self.game_height + 24)
        pygame.draw.rect(self.screen, COLORS['wall'], border_rect, border_radius=20)
        
        inner_rect = pygame.Rect(x, y, self.game_width, self.game_height)
        pygame.draw.rect(self.screen, COLORS['background'], inner_rect, border_radius=12)

    def draw_snake(self, surface, snake, invincible=False):
        """Draw the snake with optional invincibility effect"""
        if len(snake.body) < 2:
            return
        
        # Get directions for head and tail
        head_dir = self.get_head_direction(snake.body)
        tail_dir = self.get_tail_direction(snake.body)
        
        # Draw each segment
        for i, segment in enumerate(snake.body):
            segment_rect = pygame.Rect(
                segment[0] * self.cell_size,
                segment[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            
            # Apply invincibility effect (pulsing transparency)
            if invincible:
                pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 to 1 pulsing value
                
                # Create a temporary surface with per-pixel alpha
                temp_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                
                # Draw the appropriate sprite based on segment position
                if i == 0:  # Head
                    head_sprite = pygame.transform.scale(self.sprites['head'][head_dir], (self.cell_size, self.cell_size))
                    temp_surface.blit(head_sprite, (0, 0))
                elif i == len(snake.body) - 1:  # Tail
                    tail_sprite = pygame.transform.scale(self.sprites['tail'][tail_dir], (self.cell_size, self.cell_size))
                    temp_surface.blit(tail_sprite, (0, 0))
                else:  # Body
                    prev = snake.body[i-1]
                    curr = snake.body[i]
                    next_seg = snake.body[i+1]
                    body_sprite = self.get_body_sprite(prev, curr, next_seg)
                    body_sprite = pygame.transform.scale(body_sprite, (self.cell_size, self.cell_size))
                    temp_surface.blit(body_sprite, (0, 0))
                
                # Apply pulsing alpha effect
                alpha_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, int(150 + 105 * pulse)))
                temp_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                surface.blit(temp_surface, segment_rect)
            else:
                # Normal snake drawing with sprites
                if i == 0:  # Head
                    head_sprite = pygame.transform.scale(self.sprites['head'][head_dir], (self.cell_size, self.cell_size))
                    surface.blit(head_sprite, segment_rect)
                elif i == len(snake.body) - 1:  # Tail
                    tail_sprite = pygame.transform.scale(self.sprites['tail'][tail_dir], (self.cell_size, self.cell_size))
                    surface.blit(tail_sprite, segment_rect)
                else:  # Body
                    prev = snake.body[i-1]
                    curr = snake.body[i]
                    next_seg = snake.body[i+1]
                    body_sprite = self.get_body_sprite(prev, curr, next_seg)
                    body_sprite = pygame.transform.scale(body_sprite, (self.cell_size, self.cell_size))
                    surface.blit(body_sprite, segment_rect)

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

    def update_display(self, snake, food_pos, score, paused, difficulty='medium', powerup=None, active_effects=None):
        if active_effects is None:
            active_effects = {}
            
        # Draw gradient background
        self.screen.blit(pygame.transform.scale(self.gradient_bg, self.current_size), (0, 0))
        
        # Calculate game area position - fixed at center with offset for UI
        game_x = (self.current_size[0] - self.game_width) // 2
        game_y = (self.current_size[1] - self.game_height) // 2 + 30  # Move game area down slightly for UI
        
        # Draw decorative border around game area
        game_rect = pygame.Rect(
            game_x - 10,
            game_y - 10,
            self.game_width + 20,
            self.game_height + 20
        )
        
        # Draw outer glow effect
        for i in range(5, 0, -1):
            glow_rect = game_rect.inflate(i*4, i*4)
            alpha = 100 - i * 15
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            s.fill((COLORS[difficulty][0], COLORS[difficulty][1], COLORS[difficulty][2], alpha))
            self.screen.blit(s, glow_rect)
        
        # Draw main border
        pygame.draw.rect(self.screen, COLORS['wall'], game_rect, border_radius=15)
        
        # Draw inner game area
        inner_rect = pygame.Rect(
            game_x,
            game_y,
            self.game_width,
            self.game_height
        )
        pygame.draw.rect(self.screen, COLORS['background'], inner_rect, border_radius=8)
        
        # Create game surface
        game_surface = pygame.Surface((self.game_width, self.game_height))
        game_surface.fill(COLORS['background'])
        
        # Draw food
        food_rect = pygame.Rect(
            food_pos[0] * self.cell_size,
            food_pos[1] * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        food_sprite = pygame.transform.scale(self.sprites['apple'], (self.cell_size, self.cell_size))
        game_surface.blit(food_sprite, food_rect)
        
        # Draw power-up if active
        if powerup and powerup.active:
            powerup_rect = pygame.Rect(
                powerup.position[0] * self.cell_size,
                powerup.position[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(game_surface, powerup.get_color(), powerup_rect)
            
            # Draw a pulsing effect
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 to 1 pulsing value
            inner_rect = powerup_rect.inflate(-self.cell_size * 0.4 * pulse, -self.cell_size * 0.4 * pulse)
            pygame.draw.rect(game_surface, COLORS['background'], inner_rect)
        
        # Draw snake
        self.draw_snake(game_surface, snake, 'invincibility' in active_effects)
        
        # Blit game surface to screen at the fixed position
        self.screen.blit(game_surface, (game_x, game_y))
        
        # Draw UI panel at the top
        ui_panel_height = 60
        ui_panel = pygame.Rect(0, 0, self.current_size[0], ui_panel_height)
        s = pygame.Surface((ui_panel.width, ui_panel.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(s, ui_panel)
        
        # Draw score with shadow effect
        score_text = f"Score: {score}"
        # Draw shadow
        draw_text(self.screen, score_text, self.score_font, (0, 0, 0, 150), 
                 self.current_size[0] // 4 + 2, ui_panel_height // 2 + 2)
        # Draw text
        draw_text(self.screen, score_text, self.score_font, COLORS['score_text'], 
                 self.current_size[0] // 4, ui_panel_height // 2)
        
        # Draw difficulty with shadow effect
        diff_text = f"Difficulty: {difficulty.capitalize()}"
        # Draw shadow
        draw_text(self.screen, diff_text, self.font, (0, 0, 0, 150), 
                 self.current_size[0] * 3 // 4 + 2, ui_panel_height // 2 + 2)
        # Draw text
        draw_text(self.screen, diff_text, self.font, COLORS[difficulty], 
                 self.current_size[0] * 3 // 4, ui_panel_height // 2)
        
        # Draw active effects panel on the right side
        if active_effects:
            panel_width = 200
            panel_height = len(active_effects) * 40 + 20
            panel_x = self.current_size[0] - panel_width - 20
            panel_y = ui_panel_height + 20
            
            # Draw panel background
            effect_panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            s = pygame.Surface((effect_panel.width, effect_panel.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))  # Semi-transparent black
            self.screen.blit(s, effect_panel)
            
            # Draw panel border
            pygame.draw.rect(self.screen, COLORS['wall'], effect_panel, width=2, border_radius=8)
            
            # Draw effects
            y_pos = panel_y + 20
            for effect in active_effects:
                effect_text = f"{effect.replace('_', ' ').title()}: {active_effects[effect]}"
                effect_color = powerup.types[effect]['color'] if powerup and effect in powerup.types else COLORS['text']
                # Draw shadow
                draw_text(self.screen, effect_text, self.font, (0, 0, 0, 150), 
                         panel_x + panel_width // 2 + 2, y_pos + 2)
                # Draw text
                draw_text(self.screen, effect_text, self.font, effect_color, 
                         panel_x + panel_width // 2, y_pos)
                y_pos += 40
        
        # Draw pause message if paused
        if paused:
            # Create semi-transparent overlay
            overlay = pygame.Surface(self.current_size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Semi-transparent black
            self.screen.blit(overlay, (0, 0))
            
            # Draw pause text with shadow
            pause_text = "PAUSED"
            # Draw shadow
            draw_text(self.screen, pause_text, self.title_font, (0, 0, 0, 200), 
                     self.current_size[0] // 2 + 3, self.current_size[1] // 2 - 27)
            # Draw text
            draw_text(self.screen, pause_text, self.title_font, COLORS['text'], 
                     self.current_size[0] // 2, self.current_size[1] // 2 - 30)
            
            # Draw instruction
            instruction = "Press SPACE to continue"
            # Draw shadow
            draw_text(self.screen, instruction, self.font, (0, 0, 0, 200), 
                     self.current_size[0] // 2 + 2, self.current_size[1] // 2 + 22)
            # Draw text
            draw_text(self.screen, instruction, self.font, COLORS['text'], 
                     self.current_size[0] // 2, self.current_size[1] // 2 + 20)
        
        pygame.display.flip()
        self.clock.tick(60)

    def create_button(self, y_pos, text, width=200):
        button_x = self.current_size[0] // 2 - width // 2
        return Button(button_x, y_pos, width, 50, text)

    def main_menu(self):
        # Draw gradient background
        self.screen.blit(pygame.transform.scale(self.gradient_bg, self.current_size), (0, 0))
        
        # Draw decorative elements with faster animation
        self.draw_decorative_elements(animation_speed=2)
        
        # Calculate positions based on screen size
        title_y = self.current_size[1] * 0.15  # 15% from the top
        
        # Draw title with enhanced glow effect
        # Draw glow
        for i in range(5, 0, -1):
            glow_color = (100, 100, 200, 50 - i * 8)
            draw_text(self.screen, "SNAKE GAME", self.title_font, glow_color, 
                     self.current_size[0] // 2 + i, title_y + i)
        
        # Draw shadow
        draw_text(self.screen, "SNAKE GAME", self.title_font, (0, 0, 0, 150), 
                 self.current_size[0] // 2 + 3, title_y + 3)
        
        # Draw main title
        draw_text(self.screen, "SNAKE GAME", self.title_font, COLORS['text'], 
                 self.current_size[0] // 2, title_y)
        
        # Create buttons with enhanced style - positions based on screen size
        button_width, button_height = min(220, self.current_size[0] * 0.3), 55
        button_x = self.current_size[0] // 2 - button_width // 2
        
        # Calculate optimal button spacing based on screen height
        button_area_start = title_y + 80  # Start 80px below title
        button_spacing = 20  # Fixed 20px spacing between buttons
        
        # Position buttons
        play_button = Button(button_x, button_area_start, button_width, button_height, "Play Game")
        difficulty_button = Button(button_x, button_area_start + button_height + button_spacing, 
                                  button_width, button_height, "Difficulty")
        highscore_button = Button(button_x, button_area_start + 2 * (button_height + button_spacing), 
                                 button_width, button_height, "High Scores")
        quit_button = Button(button_x, button_area_start + 3 * (button_height + button_spacing), 
                            button_width, button_height, "Quit")
        
        # Customize button appearance
        for btn in [play_button, difficulty_button, highscore_button, quit_button]:
            btn.base_color = (60, 60, 80)
            btn.hover_color = (80, 80, 120)
            btn.current_color = btn.base_color
        
        buttons = [play_button, difficulty_button, highscore_button, quit_button]
        
        return buttons

    def draw_decorative_elements(self, animation_speed=1):
        """Draw decorative elements on the screen
        
        Args:
            animation_speed: Speed multiplier for the animation (higher = faster)
        """
        # Use a time-based approach for controlled movement
        current_time = pygame.time.get_ticks() // (200 // animation_speed)  # Adjust speed
        
        # Draw some decorative snake-like patterns
        for i in range(5):
            # Use deterministic positions based on time for controlled movement
            seed = i * 1000 + current_time // 5  # Control movement speed
            random.seed(seed)
            
            start_x = random.randint(0, self.current_size[0])
            start_y = random.randint(0, self.current_size[1])
            length = random.randint(5, 15)
            color = (random.randint(30, 70), random.randint(30, 70), random.randint(60, 120), 100)
            
            points = [(start_x, start_y)]
            for j in range(length):
                last_x, last_y = points[-1]
                # Use deterministic direction choice
                direction_seed = seed + j
                random.seed(direction_seed)
                direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                new_x = last_x + direction[0] * 20
                new_y = last_y + direction[1] * 20
                points.append((new_x, new_y))
            
            if len(points) > 1:
                pygame.draw.lines(self.screen, color, False, points, 8)
        
        # Reset the random seed
        random.seed()

    def difficulty_menu(self):
        # Draw gradient background
        self.screen.blit(pygame.transform.scale(self.gradient_bg, self.current_size), (0, 0))
        
        # Draw decorative elements
        self.draw_decorative_elements(animation_speed=1.5)
        
        # Calculate positions based on screen size
        title_y = self.current_size[1] * 0.15  # 15% from the top
        
        # Draw title with enhanced glow effect
        # Draw glow
        for i in range(5, 0, -1):
            glow_color = (100, 100, 200, 50 - i * 8)
            draw_text(self.screen, "SELECT DIFFICULTY", self.title_font, glow_color, 
                     self.current_size[0] // 2 + i, title_y + i)
        
        # Draw shadow
        draw_text(self.screen, "SELECT DIFFICULTY", self.title_font, (0, 0, 0, 150), 
                 self.current_size[0] // 2 + 3, title_y + 3)
        
        # Draw main title
        draw_text(self.screen, "SELECT DIFFICULTY", self.title_font, COLORS['text'], 
                 self.current_size[0] // 2, title_y)
        
        # Create buttons - positions based on screen size
        button_width, button_height = min(220, self.current_size[0] * 0.3), 55
        button_x = self.current_size[0] // 2 - button_width // 2
        button_spacing = 20  # Fixed 20px spacing between buttons
        button_area_start = title_y + 80  # Start 80px below title
        
        easy_button = Button(button_x, button_area_start, button_width, button_height, "Easy")
        medium_button = Button(button_x, button_area_start + button_height + button_spacing, 
                              button_width, button_height, "Medium")
        hard_button = Button(button_x, button_area_start + 2 * (button_height + button_spacing), 
                            button_width, button_height, "Hard")
        back_button = Button(button_x, button_area_start + 3 * (button_height + button_spacing), 
                            button_width, button_height, "Back")
        
        # Set button colors based on difficulty
        easy_button.base_color = COLORS['easy']
        easy_button.hover_color = tuple(min(c + 40, 255) for c in COLORS['easy'])
        easy_button.current_color = easy_button.base_color
        
        medium_button.base_color = COLORS['medium']
        medium_button.hover_color = tuple(min(c + 40, 255) for c in COLORS['medium'])
        medium_button.current_color = medium_button.base_color
        
        hard_button.base_color = COLORS['hard']
        hard_button.hover_color = tuple(min(c + 40, 255) for c in COLORS['hard'])
        hard_button.current_color = hard_button.base_color
        
        buttons = [easy_button, medium_button, hard_button, back_button]
        
        return buttons

    def game_over(self, score):
        # Draw gradient background
        self.screen.blit(pygame.transform.scale(self.gradient_bg, self.current_size), (0, 0))
        
        # Draw decorative elements
        self.draw_decorative_elements(animation_speed=1.5)
        
        # Draw dramatic overlay with pulsing effect
        overlay = pygame.Surface(self.current_size, pygame.SRCALPHA)
        pulse = abs(pygame.time.get_ticks() % 2000 - 1000) / 1000  # 0 to 1 pulsing value
        overlay_alpha = 100 + int(50 * pulse)  # Pulsing alpha value
        overlay.fill((50, 0, 0, overlay_alpha))  # Red-tinted overlay
        self.screen.blit(overlay, (0, 0))
        
        # Calculate positions based on screen size
        title_y = self.current_size[1] * 0.15  # 15% from the top
        
        # Draw title with dramatic glow effect
        # Draw dramatic red glow
        for i in range(8, 0, -1):
            glow_alpha = 30 - i * 3
            glow_size = i * 3
            glow_color = (200 + min(55, i * 7), 0, 0, glow_alpha)
            draw_text(self.screen, "GAME OVER", self.title_font, glow_color, 
                     self.current_size[0] // 2 + glow_size, title_y + glow_size)
            draw_text(self.screen, "GAME OVER", self.title_font, glow_color, 
                     self.current_size[0] // 2 - glow_size, title_y + glow_size)
            draw_text(self.screen, "GAME OVER", self.title_font, glow_color, 
                     self.current_size[0] // 2 + glow_size, title_y - glow_size)
            draw_text(self.screen, "GAME OVER", self.title_font, glow_color, 
                     self.current_size[0] // 2 - glow_size, title_y - glow_size)
        
        # Draw shadow
        draw_text(self.screen, "GAME OVER", self.title_font, (0, 0, 0, 200), 
                 self.current_size[0] // 2 + 3, title_y + 3)
        
        # Draw main title with pulsing color
        title_color_pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 to 1 pulsing value
        title_red = 200 + int(55 * title_color_pulse)
        title_color = (title_red, 50, 50)
        draw_text(self.screen, "GAME OVER", self.title_font, title_color, 
                 self.current_size[0] // 2, title_y)
        
        # Draw score panel - size based on screen dimensions
        panel_width = min(350, self.current_size[0] * 0.5)  # 50% of screen width, max 350px
        panel_height = min(120, self.current_size[1] * 0.2)  # 20% of screen height, max 120px
        panel_x = self.current_size[0] // 2 - panel_width // 2
        panel_y = title_y + 80  # 80px below title
        
        # Draw panel with glow
        for i in range(5, 0, -1):
            glow_rect = pygame.Rect(panel_x - i*3, panel_y - i*3, 
                                   panel_width + i*6, panel_height + i*6)
            glow_alpha = 50 - i * 8
            pygame.draw.rect(self.screen, (200, 50, 50, glow_alpha), glow_rect, 
                            border_radius=15)
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((40, 10, 10, 180))
        self.screen.blit(panel_surface, panel_rect)
        
        # Draw panel border
        pygame.draw.rect(self.screen, (200, 50, 50), panel_rect, width=2, border_radius=10)
        
        # Draw score with enhanced effects
        score_y = panel_y + panel_height * 0.5  # Center in panel
        score_text = f"SCORE: {score}"
        
        # Draw score label
        draw_text(self.screen, "FINAL", self.font, (200, 200, 200), 
                 self.current_size[0] // 2, panel_y + panel_height * 0.25)
        
        # Draw score glow
        for i in range(4, 0, -1):
            glow_color = (200, 150, 50, 50 - i * 10)
            draw_text(self.screen, score_text, self.score_font, glow_color, 
                     self.current_size[0] // 2 + i, score_y + i)
            draw_text(self.screen, score_text, self.score_font, glow_color, 
                     self.current_size[0] // 2 - i, score_y + i)
        
        # Draw score shadow
        draw_text(self.screen, score_text, self.score_font, (0, 0, 0, 150), 
                 self.current_size[0] // 2 + 2, score_y + 2)
        
        # Draw score
        draw_text(self.screen, score_text, self.score_font, COLORS['score_text'], 
                 self.current_size[0] // 2, score_y)
        
        # Create buttons with enhanced style - positions based on screen size
        button_width, button_height = min(220, self.current_size[0] * 0.3), 55
        button_x = self.current_size[0] // 2 - button_width // 2
        
        # Calculate optimal button spacing
        button_area_start = panel_y + panel_height + 30  # 30px below panel
        button_spacing = 20  # Fixed 20px spacing between buttons
        
        # Ensure buttons are visible on screen
        max_second_button_y = self.current_size[1] - button_height - 20
        if button_area_start + button_height + button_spacing + button_height > max_second_button_y:
            # Adjust spacing if screen is too small
            button_spacing = 10  # Reduce to minimum spacing
        
        restart_button = Button(button_x, button_area_start, button_width, button_height, "Play Again")
        menu_button = Button(button_x, button_area_start + button_height + button_spacing, 
                            button_width, button_height, "Main Menu")
        
        # Customize button appearance
        for btn in [restart_button, menu_button]:
            btn.base_color = (60, 30, 30)
            btn.hover_color = (100, 40, 40)
            btn.current_color = btn.base_color
            
            # Add glow to buttons
            button_rect = pygame.Rect(btn.rect)
            for i in range(3, 0, -1):
                glow_rect = button_rect.inflate(i*4, i*4)
                pygame.draw.rect(self.screen, (200, 50, 50, 70 - i * 20), glow_rect, 
                                border_radius=8)
            
            btn.draw(self.screen)
        
        pygame.display.flip()
        return [restart_button, menu_button]

    def display_highscores(self, highscores):
        # Draw gradient background
        self.screen.blit(pygame.transform.scale(self.gradient_bg, self.current_size), (0, 0))
        
        # Draw decorative elements
        self.draw_decorative_elements(animation_speed=1.5)
        
        # Draw semi-transparent overlay for better readability
        overlay = pygame.Surface(self.current_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 50))  # Very light black overlay
        self.screen.blit(overlay, (0, 0))
        
        # Calculate positions based on screen size
        title_y = self.current_size[1] * 0.1  # 10% from the top
        
        # Draw title with enhanced glow effect
        # Draw glow
        for i in range(5, 0, -1):
            glow_color = (200, 200, 50, 50 - i * 8)
            draw_text(self.screen, "HIGH SCORES", self.title_font, glow_color, 
                     self.current_size[0] // 2 + i, title_y + i)
        
        # Draw shadow
        draw_text(self.screen, "HIGH SCORES", self.title_font, (0, 0, 0, 150), 
                 self.current_size[0] // 2 + 3, title_y + 3)
        
        # Draw main title
        draw_text(self.screen, "HIGH SCORES", self.title_font, COLORS['highscore_text'], 
                 self.current_size[0] // 2, title_y)
        
        # Draw main highscore panel - size based on screen dimensions
        panel_width = min(400, self.current_size[0] * 0.6)  # 60% of screen width, max 400px
        max_panel_height = self.current_size[1] * 0.65  # 65% of screen height
        panel_height = min(len(highscores) * 45 + 40, max_panel_height)
        panel_x = self.current_size[0] // 2 - panel_width // 2
        panel_y = title_y + 60  # 60px below title
        
        # Draw panel background with gradient
        score_panel = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        
        # Create gradient for panel
        for y in range(int(panel_height)):
            alpha = 150 - y * 30 // int(panel_height)
            pygame.draw.line(panel_surface, (30, 30, 50, max(100, alpha)), 
                            (0, y), (panel_width, y))
        
        self.screen.blit(panel_surface, score_panel)
        
        # Draw panel border with glow
        for i in range(3, 0, -1):
            border_rect = score_panel.inflate(i*4, i*4)
            pygame.draw.rect(self.screen, (200, 200, 50, 70 - i * 20), border_rect, 
                            width=2, border_radius=10)
        
        pygame.draw.rect(self.screen, COLORS['highscore_text'], score_panel, 
                        width=2, border_radius=10)
        
        # Draw header
        header_y = panel_y + 20
        header_rect = pygame.Rect(panel_x + 10, header_y - 10, panel_width - 20, 40)
        pygame.draw.rect(self.screen, (50, 50, 70, 150), header_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['highscore_text'], header_rect, 
                        width=1, border_radius=5)
        
        # Draw header text
        draw_text(self.screen, "RANK", self.font, COLORS['highscore_text'], 
                 panel_x + panel_width * 0.2, header_y)
        draw_text(self.screen, "SCORE", self.font, COLORS['highscore_text'], 
                 panel_x + panel_width * 0.7, header_y)
        
        # Calculate how many scores can fit in the panel
        row_height = 40  # Reduce row height from 45 to 40
        visible_rows = int((panel_height - 60) / row_height)
        
        # Initialize scrolling variables
        scroll_offset = 0
        max_scroll = max(0, len(highscores) - visible_rows)
        
        # Create scroll buttons if needed
        scroll_up_btn = None
        scroll_down_btn = None
        
        if max_scroll > 0:
            # Create scroll buttons
            scroll_btn_size = 30
            scroll_up_btn = Button(
                panel_x + panel_width - scroll_btn_size - 10, 
                panel_y + 60, 
                scroll_btn_size, 
                scroll_btn_size, 
                "▲"
            )
            scroll_down_btn = Button(
                panel_x + panel_width - scroll_btn_size - 10, 
                panel_y + panel_height - scroll_btn_size - 10, 
                scroll_btn_size, 
                scroll_btn_size, 
                "▼"
            )
            
            # Style scroll buttons
            for btn in [scroll_up_btn, scroll_down_btn]:
                btn.base_color = (60, 60, 80)
                btn.hover_color = (80, 80, 120)
                btn.current_color = btn.base_color
        
        # Create back button with enhanced style - positioned relative to panel
        button_width, button_height = min(220, self.current_size[0] * 0.3), 55
        button_x = self.current_size[0] // 2 - button_width // 2
        button_y = panel_y + panel_height + 20  # 20px below panel
        
        # Ensure button is visible on screen
        max_button_y = self.current_size[1] - button_height - 10
        button_y = min(button_y, max_button_y)
        
        back_button = Button(button_x, button_y, button_width, button_height, "Back")
        back_button.base_color = (60, 60, 80)
        back_button.hover_color = (80, 80, 120)
        back_button.current_color = back_button.base_color
        
        # Add glow to button
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        for i in range(3, 0, -1):
            glow_rect = button_rect.inflate(i*4, i*4)
            pygame.draw.rect(self.screen, (100, 100, 200, 70 - i * 20), glow_rect, 
                            border_radius=8)
        
        back_button.draw(self.screen)
        
        # Draw scroll buttons if needed
        if scroll_up_btn and scroll_down_btn:
            scroll_up_btn.draw(self.screen)
            scroll_down_btn.draw(self.screen)
            
            # Draw scroll indicators
            if scroll_offset > 0:
                # Draw "more above" indicator
                pygame.draw.polygon(self.screen, COLORS['highscore_text'], 
                                   [(panel_x + panel_width // 2 - 10, panel_y + 50),
                                    (panel_x + panel_width // 2 + 10, panel_y + 50),
                                    (panel_x + panel_width // 2, panel_y + 40)])
            
            if scroll_offset < max_scroll:
                # Draw "more below" indicator
                pygame.draw.polygon(self.screen, COLORS['highscore_text'], 
                                   [(panel_x + panel_width // 2 - 10, panel_y + panel_height - 10),
                                    (panel_x + panel_width // 2 + 10, panel_y + panel_height - 10),
                                    (panel_x + panel_width // 2, panel_y + panel_height)])
        
        # Handle scrolling and interaction
        clock = pygame.time.Clock()
        running = True
        
        while running and not pygame.event.get(pygame.QUIT):
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw scores with enhanced style - only visible rows
            content_surface = pygame.Surface((panel_width - 20, panel_height - 60), pygame.SRCALPHA)
            
            for i in range(len(highscores)):
                if i < scroll_offset or i >= scroll_offset + visible_rows:
                    continue
                    
                # Calculate position in the visible area
                rel_idx = i - scroll_offset
                y_pos = rel_idx * row_height + 10
                
                # Draw score row
                row_rect = pygame.Rect(0, y_pos, panel_width - 20, 35)  # Reduce height from 40 to 35
                
                # Alternate colors for better readability
                if i % 2 == 0:
                    row_color = (40, 40, 60, 150)
                else:
                    row_color = (50, 50, 70, 150)
                    
                # Highlight top 3 scores
                if i < 3:
                    # Gold, Silver, Bronze colors
                    highlight_colors = [
                        (255, 215, 0, 100),  # Gold
                        (192, 192, 192, 100),  # Silver
                        (205, 127, 50, 100)   # Bronze
                    ]
                    row_color = highlight_colors[i]
                
                pygame.draw.rect(content_surface, row_color, row_rect, border_radius=5)
                
                # Draw rank with medal for top 3
                if i < 3:
                    medal_symbols = ["🥇", "🥈", "🥉"]
                    rank_text = f"{i+1}  {medal_symbols[i]}"
                else:
                    rank_text = f"{i+1}"
                    
                # Draw rank
                draw_text(content_surface, rank_text, self.score_font, COLORS['text'], 
                         panel_width * 0.2 - 10, y_pos + 17)  # Center vertically
                
                # Draw score with glow for top 3
                if i < 3:
                    # Draw glow
                    for j in range(2, 0, -1):
                        draw_text(content_surface, f"{highscores[i]}", self.score_font, 
                                 (highlight_colors[i][0], highlight_colors[i][1], highlight_colors[i][2], 150), 
                                 panel_width * 0.7 - 10 + j, y_pos + 17 + j)
                
                # Draw score
                draw_text(content_surface, f"{highscores[i]}", self.score_font, COLORS['score_text'], 
                         panel_width * 0.7 - 10, y_pos + 17)  # Center vertically
            
            # Blit content surface to screen
            self.screen.blit(content_surface, (panel_x + 10, panel_y + 60))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return back_button
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check back button click
                    if back_button.check_click(mouse_pos):
                        return back_button
                    
                    # Check scroll button clicks
                    if scroll_up_btn and scroll_up_btn.check_click(mouse_pos) and scroll_offset > 0:
                        scroll_offset -= 1
                        # Redraw the screen
                        self.screen.blit(panel_surface, score_panel)
                        pygame.draw.rect(self.screen, COLORS['highscore_text'], score_panel, 
                                        width=2, border_radius=10)
                        pygame.draw.rect(self.screen, (50, 50, 70, 150), header_rect, border_radius=5)
                        pygame.draw.rect(self.screen, COLORS['highscore_text'], header_rect, 
                                        width=1, border_radius=5)
                        draw_text(self.screen, "RANK", self.font, COLORS['highscore_text'], 
                                 panel_x + panel_width * 0.2, header_y)
                        draw_text(self.screen, "SCORE", self.font, COLORS['highscore_text'], 
                                 panel_x + panel_width * 0.7, header_y)
                    
                    if scroll_down_btn and scroll_down_btn.check_click(mouse_pos) and scroll_offset < max_scroll:
                        scroll_offset += 1
                        # Redraw the screen
                        self.screen.blit(panel_surface, score_panel)
                        pygame.draw.rect(self.screen, COLORS['highscore_text'], score_panel, 
                                        width=2, border_radius=10)
                        pygame.draw.rect(self.screen, (50, 50, 70, 150), header_rect, border_radius=5)
                        pygame.draw.rect(self.screen, COLORS['highscore_text'], header_rect, 
                                        width=1, border_radius=5)
                        draw_text(self.screen, "RANK", self.font, COLORS['highscore_text'], 
                                 panel_x + panel_width * 0.2, header_y)
                        draw_text(self.screen, "SCORE", self.font, COLORS['highscore_text'], 
                                 panel_x + panel_width * 0.7, header_y)
                
                # Handle mouse wheel scrolling
                elif event.type == pygame.MOUSEWHEEL:
                    if score_panel.collidepoint(mouse_pos):
                        if event.y > 0 and scroll_offset > 0:  # Scroll up
                            scroll_offset -= 1
                        elif event.y < 0 and scroll_offset < max_scroll:  # Scroll down
                            scroll_offset += 1
            
            # Update hover states for buttons
            back_button.check_hover(mouse_pos)
            back_button.draw(self.screen)
            
            if scroll_up_btn and scroll_down_btn:
                scroll_up_btn.check_hover(mouse_pos)
                scroll_down_btn.check_hover(mouse_pos)
                scroll_up_btn.draw(self.screen)
                scroll_down_btn.draw(self.screen)
                
                # Draw scroll indicators
                if scroll_offset > 0:
                    # Draw "more above" indicator
                    pygame.draw.polygon(self.screen, COLORS['highscore_text'], 
                                       [(panel_x + panel_width // 2 - 10, panel_y + 50),
                                        (panel_x + panel_width // 2 + 10, panel_y + 50),
                                        (panel_x + panel_width // 2, panel_y + 40)])
                
                if scroll_offset < max_scroll:
                    # Draw "more below" indicator
                    pygame.draw.polygon(self.screen, COLORS['highscore_text'], 
                                       [(panel_x + panel_width // 2 - 10, panel_y + panel_height - 10),
                                        (panel_x + panel_width // 2 + 10, panel_y + panel_height - 10),
                                        (panel_x + panel_width // 2, panel_y + panel_height)])
            
            pygame.display.flip()
            clock.tick(30)
        
        return back_button