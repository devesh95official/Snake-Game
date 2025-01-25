class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Start with 3 segments moving upward
        self.body = [(10, 10), (10, 11), (10, 12)]
        self.direction = (0, -1)  # Up
        self.new_direction = (0, -1)
        self.grow = False

    def change_direction(self, new_dir):
        # Prevent 180-degree turns
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.new_direction = new_dir

    def move(self):
        self.direction = self.new_direction
        new_head = (
            (self.body[0][0] + self.direction[0]) % 20,
            (self.body[0][1] + self.direction[1]) % 20
        )
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def check_collision(self):
        # Check if head collides with any body segment
        return self.body[0] in self.body[1:]