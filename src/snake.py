class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = (1, 0)
        self.new_direction = (1, 0)
        self.grow = False

    def change_direction(self, new_dir):
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
        return len(self.body) != len(set(self.body))