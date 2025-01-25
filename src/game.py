import pygame
from snake import Snake
from food import Food
from controller import GameController
from view import GameView
from config import FPS, CELL_SIZE
from utils import load_highscore, save_highscore

class Game:
    def __init__(self):
        self.controller = GameController()
        self.view = GameView()
        self.highscore = load_highscore()
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    def check_food_collision(self):
        if self.snake.body[-1].distance_to(self.food.position) < CELL_SIZE:
            self.snake.grow = True
            self.food.randomize_position()
            self.score += 1
            if self.score > self.highscore:
                self.highscore = self.score
                save_highscore(self.highscore)

    def run_game(self):
        while self.running and not self.controller.quit:
            self.controller.handle_input(self.snake)
            
            if not self.controller.paused:
                self.snake.update()
                self.check_food_collision()
                
                if self.snake.check_collision():
                    self.show_game_over()
                    return

            try:
                self.view.update_display(self.snake, self.food, self.score)
            except pygame.error:
                self.controller.quit = True
                return

    def show_game_over(self):
        restart_btn, menu_btn = self.view.game_over(self.score)
        pygame.display.flip()
        pygame.time.wait(500)  # Prevent instant click-through
        
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.rect.collidepoint(mouse_pos):
                        self.reset_game()
                        self.run_game()
                        return
                    elif menu_btn.rect.collidepoint(mouse_pos):
                        return

    def main_menu(self):
        while not self.controller.quit:
            mouse_pos = pygame.mouse.get_pos()
            play_btn, exit_btn = self.view.main_menu(self.highscore)
            
            play_btn.check_hover(mouse_pos)
            exit_btn.check_hover(mouse_pos)
            play_btn.draw(self.view.screen)
            exit_btn.draw(self.view.screen)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.controller.quit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.rect.collidepoint(mouse_pos):
                        self.reset_game()
                        self.run_game()
                    elif exit_btn.rect.collidepoint(mouse_pos):
                        self.controller.quit = True

if __name__ == "__main__":
    game = Game()
    game.main_menu()
    pygame.quit()