import pygame
from snake import Snake
from food import Food
from controller import GameController
from view import GameView
from config import GRID_SIZE
from utils import load_highscores, save_highscore

class Game:
    def __init__(self):
        self.controller = GameController()
        self.view = GameView()
        self.highscores = load_highscores()
        self.reset_game()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(GRID_SIZE)
        self.score = 0
        self.running = True

    def check_food_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.food.randomize_position(self.snake.body)
            self.score += 1
            if self.score > self.highscores[-1]:
                save_highscore(self.score)
                self.highscores = load_highscores()

    def run_game(self):
        while self.running and not self.controller.quit:
            if self.controller.resize_event:
                self.view.handle_resize(self.controller.resize_event)
                self.controller.resize_event = None
                
            self.controller.handle_input(self.snake, self.view)
            
            if not self.controller.paused:
                self.snake.move()
                self.check_food_collision()
                
                if self.snake.check_collision():
                    self.show_game_over()
                    return

            self.view.update_display(self.snake, self.food.position, self.score, self.controller.paused)

    def show_game_over(self):
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

    def main_menu(self):
        while not self.controller.quit:
            buttons = self.view.main_menu()
            mouse_pos = pygame.mouse.get_pos()
            
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
                        self.show_highscores()
                    elif buttons[2].check_click(mouse_pos):
                        self.controller.quit = True

if __name__ == "__main__":
    game = Game()
    game.main_menu()
    pygame.quit()