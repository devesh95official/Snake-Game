# Snake Game

An advanced Python implementation of the classic Snake game using Pygame.

## Version 1.5

### Features

- Classic snake gameplay with modern graphics
- Multiple difficulty levels (Easy, Medium, Hard)
- Power-ups with special effects:
  - Speed Boost: Temporarily increases snake speed
  - Slow Motion: Temporarily decreases snake speed
  - Double Points: Temporarily doubles points earned
  - Invincibility: Temporarily prevents death from self-collision
- Highscore tracking
- Responsive design that adapts to window size
- Pause functionality

### Controls

- Arrow keys or WASD to move the snake
- Space to pause/unpause the game
- Mouse to navigate menus

### Requirements

- Python 3.6+
- Pygame 2.5.2

### Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```

### Project Structure

- `main.py`: Entry point for the game
- `src/`: Source code directory
  - `game.py`: Main game logic
  - `snake.py`: Snake class
  - `food.py`: Food class
  - `powerup.py`: Power-up class
  - `view.py`: Rendering and UI
  - `controller.py`: Input handling
  - `config.py`: Game settings
  - `utils.py`: Helper functions
- `assets/`: Game assets
  - `sprites/`: Game sprites
  - `sounds/`: Game sounds
  - `fonts/`: Game fonts
