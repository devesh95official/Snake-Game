import random
import pygame

class PowerUp:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.position = (0, 0)
        self.active = False
        self.type = None
        self.duration = 0
        self.timer = 0
        self.types = {
            'speed': {'color': (0, 255, 255), 'duration': 100, 'probability': 0.3},
            'slow': {'color': (255, 0, 255), 'duration': 100, 'probability': 0.3},
            'double_points': {'color': (255, 255, 0), 'duration': 150, 'probability': 0.2},
            'invincibility': {'color': (255, 255, 255), 'duration': 80, 'probability': 0.2}
        }

    def randomize_position(self, snake_body, food_position):
        """Place the power-up at a random position, not overlapping with snake or food"""
        while True:
            self.position = (
                random.randint(0, self.grid_size-1),
                random.randint(0, self.grid_size-1)
            )
            if self.position not in snake_body and self.position != food_position:
                break

    def spawn(self, snake_body, food_position):
        """Spawn a power-up at a random position"""
        if not self.active:
            self.randomize_position(snake_body, food_position)
            self.select_random_type()
            self.active = True
            self.timer = self.duration

    def select_random_type(self):
        """Select a random power-up type based on their probabilities"""
        total_prob = sum(info['probability'] for info in self.types.values())
        r = random.random() * total_prob
        
        cumulative = 0
        for type_name, info in self.types.items():
            cumulative += info['probability']
            if r <= cumulative:
                self.type = type_name
                self.duration = info['duration']
                break

    def update(self):
        """Update the power-up timer if active"""
        if self.active and self.timer > 0:
            self.timer -= 1
            if self.timer <= 0:
                self.deactivate()

    def deactivate(self):
        """Deactivate the power-up"""
        self.active = False
        self.type = None

    def collect(self):
        """Collect the power-up and return its type"""
        if self.active:
            collected_type = self.type
            self.active = False
            return collected_type
        return None

    def get_color(self):
        """Get the color of the current power-up"""
        if self.active and self.type in self.types:
            return self.types[self.type]['color']
        return (255, 255, 255)  # Default white

    def get_effect_description(self):
        """Return a description of the power-up effect"""
        if not self.active or not self.type:
            return ""
            
        descriptions = {
            'speed': "Speed Boost!",
            'slow': "Slow Motion!",
            'double_points': "Double Points!",
            'invincibility': "Invincibility!"
        }
        return descriptions.get(self.type, "") 