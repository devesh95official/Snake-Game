import pygame
import os
from src.snake import Snake
from src.food import Food
from src.powerup import PowerUp
from src.controller import GameController
from src.view import GameView
from src.config import GRID_SIZE, SOUNDS, SOUND_DIR, DIFFICULTY
from src.utils import load_highscores, save_highscore

class Game:
    def __init__(self):
        self.controller = GameController()
        self.view = GameView()
        self.highscores = load_highscores()
        self.load_sounds()
        self.difficulty = 'medium'  # Default difficulty
        self.reset_game()

    def load_sounds(self):
        pygame.mixer.init()
        self.sounds = {
            'eat': pygame.mixer.Sound(os.path.join(SOUND_DIR, SOUNDS['eat'])),
            'game_over': pygame.mixer.Sound(os.path.join(SOUND_DIR, SOUNDS['game_over']))
        }
        
        # Load powerup sound
        try:
            powerup_path = os.path.join(SOUND_DIR, SOUNDS['powerup'])
            if os.path.exists(powerup_path):
                self.sounds['powerup'] = pygame.mixer.Sound(powerup_path)
            else:
                # If powerup sound file doesn't exist, use eat sound as fallback
                self.sounds['powerup'] = self.sounds['eat']
        except:
            self.sounds['powerup'] = self.sounds['eat']

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(GRID_SIZE)
        self.powerup = PowerUp(GRID_SIZE)
        self.food.randomize_position(self.snake.body)
        self.score = 0
        self.apples_eaten = 0  # Track apples eaten for powerup spawning
        self.running = True
        self.fps = DIFFICULTY[self.difficulty]['fps']
        self.base_fps = self.fps
        self.score_multiplier = DIFFICULTY[self.difficulty]['multiplier']
        self.base_multiplier = self.score_multiplier
        self.active_effects = {}

    def check_food_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.food.randomize_position(self.snake.body)
            
            # Increment apples eaten counter
            self.apples_eaten += 1
            
            # Try to spawn a power-up after eating 4 apples
            if self.apples_eaten >= 4:
                self.powerup.spawn(self.snake.body, self.food.position)
                self.apples_eaten = 0  # Reset counter
            
            # Calculate score with any active multipliers
            points = 1 * self.score_multiplier
            if 'double_points' in self.active_effects:
                points *= 2
                
            self.score += points
            self.sounds['eat'].play()
            if self.score > self.highscores[-1]:
                save_highscore(self.score)
                self.highscores = load_highscores()

    def check_powerup_collision(self):
        if self.powerup.active and self.snake.body[0] == self.powerup.position:
            powerup_type = self.powerup.collect()
            if powerup_type:
                self.apply_powerup_effect(powerup_type)
                # Play the powerup sound
                self.sounds['powerup'].play()

    def apply_powerup_effect(self, powerup_type):
        # Store the effect and its timer
        self.active_effects[powerup_type] = self.powerup.types[powerup_type]['duration']
        
        # Apply immediate effects
        if powerup_type == 'speed':
            self.fps = min(self.base_fps * 1.5, 30)  # 50% speed boost, capped at 30
        elif powerup_type == 'slow':
            self.fps = max(self.base_fps * 0.5, 4)  # 50% speed reduction, minimum 4
        elif powerup_type == 'invincibility':
            # Effect is checked during collision detection
            pass
        elif powerup_type == 'double_points':
            # Effect is applied during scoring
            pass

    def update_powerup_effects(self):
        # Update all active effect timers and remove expired ones
        expired_effects = []
        
        for effect, timer in self.active_effects.items():
            self.active_effects[effect] = timer - 1
            if self.active_effects[effect] <= 0:
                expired_effects.append(effect)
        
        # Remove expired effects
        for effect in expired_effects:
            self.remove_powerup_effect(effect)
    
    def remove_powerup_effect(self, effect):
        if effect in self.active_effects:
            del self.active_effects[effect]
            
            # Reset any modified values
            if effect in ['speed', 'slow']:
                self.fps = self.base_fps

    def run_game(self):
        clock = pygame.time.Clock()
        while self.running and not self.controller.quit:
            if self.controller.resize_event:
                self.view.handle_resize(self.controller.resize_event)
                self.controller.resize_event = None
                
            self.controller.handle_input(self.snake)
            
            if not self.controller.paused:
                # Update power-up timer
                self.powerup.update()
                
                # Update active effects
                self.update_powerup_effects()
                
                # Move snake
                self.snake.move()
                
                # Check collisions
                self.check_food_collision()
                self.check_powerup_collision()
                
                # Check if snake collided with itself
                if self.snake.check_collision():
                    # If invincibility is active, ignore collision
                    if 'invincibility' not in self.active_effects:
                        self.show_game_over()
                        return

            self.view.update_display(
                self.snake, 
                self.food.position, 
                self.score, 
                self.controller.paused, 
                self.difficulty,
                self.powerup if self.powerup.active else None,
                self.active_effects
            )
            clock.tick(self.fps)

    def show_game_over(self):
        self.sounds['game_over'].play()
        buttons = self.view.game_over(self.score)
        
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].check_click(mouse_pos):
                        self.reset_game()
                        self.run_game()
                        return
                    elif buttons[1].check_click(mouse_pos):
                        return

    def show_highscores(self):
        back_btn = self.view.display_highscores(self.highscores)
        
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.check_click(mouse_pos):
                        return

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.fps = DIFFICULTY[difficulty]['fps']
        self.score_multiplier = DIFFICULTY[difficulty]['multiplier']

    def show_difficulty_menu(self):
        buttons = self.view.difficulty_menu()
        
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].check_click(mouse_pos):  # Easy
                        self.set_difficulty('easy')
                        return
                    elif buttons[1].check_click(mouse_pos):  # Medium
                        self.set_difficulty('medium')
                        return
                    elif buttons[2].check_click(mouse_pos):  # Hard
                        self.set_difficulty('hard')
                        return
                    elif buttons[3].check_click(mouse_pos):  # Back
                        return
            
            for btn in buttons:
                btn.check_hover(mouse_pos)
                btn.draw(self.view.screen)
            
            pygame.display.flip()

    def main_menu(self):
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            buttons = self.view.main_menu()
            
            for btn in buttons:
                btn.check_hover(mouse_pos)
                btn.draw(self.view.screen)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].check_click(mouse_pos):
                        self.reset_game()
                        self.run_game()
                    elif buttons[1].check_click(mouse_pos):
                        self.show_difficulty_menu()
                    elif buttons[2].check_click(mouse_pos):
                        self.show_highscores()
                    elif buttons[3].check_click(mouse_pos):
                        self.controller.quit = True

if __name__ == "__main__":
    game = Game()
    game.main_menu()
    pygame.quit()