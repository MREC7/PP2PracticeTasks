import pygame, random

CELL = 20
WIDTH, HEIGHT = 600, 400

class SnakeGame:
    def __init__(self):
        self.snake = [(100,100),(80,100),(60,100)]
        self.dir = (CELL,0)

        self.score = 0
        self.level = 1
        self.base_speed = 10

        self.active_power = None
        self.power_timer = 0

        self.obstacles = []

        self.spawn_food()
        self.spawn_poison()
        self.spawn_power()

    def rand_pos(self):
        while True:
            x = random.randint(0,(WIDTH-CELL)//CELL)*CELL
            y = random.randint(0,(HEIGHT-CELL)//CELL)*CELL
            if (x,y) not in self.snake and (x,y) not in self.obstacles:
                return (x,y)

    def spawn_food(self):
        self.food = self.rand_pos()

    def spawn_poison(self):
        self.poison = self.rand_pos()

    def spawn_power(self):
        self.power_pos = self.rand_pos()
        self.power_type = random.choice(["speed","slow","shield"])
        self.power_spawn_time = pygame.time.get_ticks()

    def move(self):
        head = (self.snake[0][0]+self.dir[0], self.snake[0][1]+self.dir[1])

        if head in self.snake or head[0]<0 or head[1]<0 or head[0]>=WIDTH or head[1]>=HEIGHT:
            if self.active_power == "shield":
                self.active_power = None
            else:
                return False, 1

        if head in self.obstacles:
            return False, 1

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 1
            self.spawn_food()

            if self.score % 4 == 0:
                self.level += 1

                if self.level >= 3:
                    self.obstacles.append(self.rand_pos())

        elif head == self.poison:
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                return False, 1
            self.spawn_poison()

        elif head == self.power_pos:
            self.active_power = self.power_type
            self.power_timer = pygame.time.get_ticks()
            self.spawn_power()

        else:
            self.snake.pop()

        if self.active_power and self.active_power != "shield":
            if pygame.time.get_ticks() - self.power_timer > 5000:
                self.active_power = None

        if pygame.time.get_ticks() - self.power_spawn_time > 8000:
            self.spawn_power()

        mod = 1
        if self.active_power == "speed":
            mod = 2
        elif self.active_power == "slow":
            mod = 0.5

        return True, mod

    def set_dir(self, d):
        if (d[0]*-1, d[1]*-1) != self.dir:
            self.dir = d