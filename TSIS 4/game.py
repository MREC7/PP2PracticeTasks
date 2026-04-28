import pygame, random

CELL = 20
WIDTH, HEIGHT = 600, 400


FOOD_QUANTITY = 3
POISON_QUANTITY = 2
POWER_QUANTITY = 2


class SnakeGame:
    def __init__(self):
        self.reset_snake()

        self.score = 0
        self.level = 1
        self.base_speed = 10

        self.active_power = None
        self.power_timer = 0

        self.obstacles = []

        self.foods = []
        self.poisons = []
        self.powers = []

        self.spawn_foods()
        self.spawn_poisons()
        self.spawn_powers()

    def reset_snake(self):
        self.snake = [(100,100),(80,100),(60,100)]
        self.dir = (CELL,0)

    def rand_pos(self):
        while True:
            x = random.randint(0,(WIDTH-CELL)//CELL)*CELL
            y = random.randint(0,(HEIGHT-CELL)//CELL)*CELL

            if (x,y) not in self.snake \
               and (x,y) not in self.obstacles \
               and (x,y) not in self.foods \
               and (x,y) not in self.poisons \
               and (x,y) not in [p["pos"] for p in self.powers]:
                return (x,y)

    

    def spawn_foods(self):
        self.foods = [self.rand_pos() for _ in range(FOOD_QUANTITY)]

    def spawn_poisons(self):
        self.poisons = [self.rand_pos() for _ in range(POISON_QUANTITY)]

    def spawn_powers(self):
        self.powers = []
        for _ in range(POWER_QUANTITY):
            self.powers.append({
                "pos": self.rand_pos(),
                "type": random.choice(["speed","slow","shield"]),
                "spawn_time": pygame.time.get_ticks()
            })

    

    def move(self):
        new_head = (
            self.snake[0][0] + self.dir[0],
            self.snake[0][1] + self.dir[1]
        )

        collision = (
            new_head in self.snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= WIDTH or new_head[1] >= HEIGHT or
            new_head in self.obstacles
        )

        
        if collision:
            if self.active_power == "shield":
                self.active_power = None
                self.reset_snake()
                return True, 1
            else:
                return False, 1

        head = new_head
        self.snake.insert(0, head)

        
        if head in self.foods:
            self.score += random.randint(1, 3)
            self.foods.remove(head)
            self.foods.append(self.rand_pos())

            if self.score % 4 == 0:
                self.level += 1
                if self.level >= 3:
                    self.obstacles.append(self.rand_pos())

        
        elif head in self.poisons:
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                return False, 1

            self.poisons.remove(head)
            self.poisons.append(self.rand_pos())

        
        else:
            picked = None
            for p in self.powers:
                if head == p["pos"]:
                    picked = p
                    break

            if picked:
                self.active_power = picked["type"]
                self.power_timer = pygame.time.get_ticks()

                self.powers.remove(picked)
                self.powers.append({
                    "pos": self.rand_pos(),
                    "type": random.choice(["speed","slow","shield"]),
                    "spawn_time": pygame.time.get_ticks()
                })
            else:
                self.snake.pop()

        
        if self.active_power:
            if pygame.time.get_ticks() - self.power_timer > 5000:
                self.active_power = None

        
        for p in self.powers:
            if pygame.time.get_ticks() - p["spawn_time"] > 8000:
                self.powers.remove(p)
                self.powers.append({
                    "pos": self.rand_pos(),
                    "type": random.choice(["speed","slow","shield"]),
                    "spawn_time": pygame.time.get_ticks()
                })
                break

        
        mod = 1
        if self.active_power == "speed":
            mod = 2
        elif self.active_power == "slow":
            mod = 0.5

        return True, mod

    def set_dir(self, d):
        if (d[0]*-1, d[1]*-1) != self.dir:
            self.dir = d