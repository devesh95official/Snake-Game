"""
Snake Game - Main entry point
"""

import pygame
from src.game import Game

def main():
    """Main entry point for the Snake Game"""
    pygame.init()
    game = Game()
    game.main_menu()
    pygame.quit()

if __name__ == "__main__":
    main() 