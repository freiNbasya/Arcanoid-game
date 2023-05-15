import random

import pgzrun
import pygame as pg


WIDTH = 800
HEIGHT = 600

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect((self.x, self. y), (self.width, self.height))

    def draw(self):
        screen.draw.filled_rect(Rect((self.x, self.y), (self.width, self.height)), (255, 255, 255))

    def update(self):
        self.x = pg.mouse.get_pos()[0]
        if self.x < -100:
            self.x = 0
        if self.x > WIDTH-50:
            self.x = WIDTH-100

    def check_collision(self, ball):
        if ball.x + ball.radius > self.x and ball.x < self.x + self.width and ball.y + ball.radius > self.y and ball.y < self.y + self.height:
        #if ball.x > self.x and ball.x < self.x + self.width and ball.y > self.y and ball.y < self.y + self.height:
            ball.VelocityY = -ball.VelocityY
    def check_collision_bonuses(self, bonus):
        global lives
        if bonus.x > self.x and bonus.x < self.x + self.width and bonus.y > self.y and bonus.y < self.y + self.height:
            bonuses.remove(bonus)
            lives += 1
    

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.VelocityX = 5
        self.VelocityY = 5

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, "Yellow")

    def update(self):
        self.x += self.VelocityX
        self.y += self.VelocityY

        if self.x > WIDTH or self.x < 0:
            self.VelocityX = -self.VelocityX
        if self.y > HEIGHT or self.y < 0:
            self.VelocityY = -self.VelocityY


class Brick:
    def __init__(self, x, y, width, height, lives, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        self.lives = lives
        self.colour = colour
        
    def draw(self):
        if self.active:
            screen.draw.filled_rect(Rect((self.x, self.y), (self.width, self.height)), self.colour)
        
    def check_collision(self, ball):
        if self.active and ball.x + ball.radius > self.x and ball.x < self.x + self.width and ball.y + ball.radius > self.y and ball.y < self.y + self.height:
        #if self.active and ball.x > self.x and ball.x < self.x + self.width and ball.y > self.y and ball.y < self.y + self.height:
            ball.VelocityY = -ball.VelocityY
            self.lives -= 1
            if self.lives == 0:
                self.active = False
                return True
        return False

class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.velocity = 100

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), 5, "Purple")

    def move(self,dt):
         self.y += self.velocity * dt



light_bricks = []
medium_bricks = []
heavy_bricks = []


for i in range(5):
    light_bricks.append(Brick(25+i*150,25*5,140,40, 1, "White"))
for j in range(5):
    medium_bricks.append(Brick(25+j*150,25*3,140,40, 2, "Blue"))
for k in range(5):
    heavy_bricks.append(Brick(25+k*150,25, 140,40, 3, "Black"))

score = 0
game_over = False
game_won = False
lives = 3
ball = Ball(400, 300, 10)
paddle = Paddle(120, 550, 100, 5)

bonuses = []


def draw():
    

    if game_over:
        screen.clear()
        if game_won:
            screen.draw.text('You won!', (360, 300), color=(255,255,255), fontsize=60)
        else:
            screen.draw.text('You lost!', (360, 300), color=(255,255,255), fontsize=60)
    else:
        screen.clear()
        screen.fill((123, 221, 65))
        screen.draw.text("Score: " + str(score), (500, 500), color=(0, 0, 0), background="white")
        for i in range(lives):
            screen.blit("hhh.png", (30*i, 300))
        ball.draw()
        paddle.draw()
        for bonus in bonuses:
            bonus.draw()
        for light_brick in light_bricks:
            light_brick.draw()
        for medium_brick in medium_bricks:
            medium_brick.draw()
        for heavy_brick in heavy_bricks:
            heavy_brick.draw()
        

def update(dt):
    global lives 
    global score
    global game_over
    global game_won
    if random.random() > 0.99:
        new_pos = random.randint(0, WIDTH)
        bonuses.append(Bonus(new_pos, 10))
    for bonus in bonuses:
        bonus.move(dt)
        
    ball.update()
    paddle.update()
    paddle.check_collision(ball)
    for bonus in bonuses:
        paddle.check_collision_bonuses(bonus)
    for light_brick in light_bricks:
        if light_brick.check_collision(ball):
            score += 1
    for medium_brick in medium_bricks:
        if medium_brick.check_collision(ball):
            score += 1
    for heavy_brick in heavy_bricks:
        if heavy_brick.check_collision(ball):
            score += 1  

    if score == len(light_bricks)+len(medium_bricks)+len(heavy_bricks):
        game_won = True
    if ball.y > HEIGHT:
        lives -= 1
        ball.x = 400
        ball.y = 300
    if lives == 0:
        game_over = True
        

  

pgzrun.go()
