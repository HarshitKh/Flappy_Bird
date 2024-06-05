import pygame
import random
import sys
import os

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)

# Load images
background_img = pygame.image.load(os.path.join("assets", "images", "background.png"))
bird_img = pygame.image.load(os.path.join("assets", "images", "bird.png"))
pipe_img = pygame.image.load(os.path.join("assets", "images", "pipe.png"))

# Load sounds
jump_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "jump.wav"))
start_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "start.wav"))
game_over_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "game_over.wav"))

font = pygame.font.Font(None, 36)

try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.4  
        self.lift = -10

    def show(self):
        screen.blit(bird_img, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > HEIGHT - 24:
            self.y = HEIGHT - 24
            self.velocity = 0

    def up(self):
        self.velocity = self.lift
        jump_sound.play()

class Pipe:
    def __init__(self):
        self.top = random.randint(50, HEIGHT//2 - 50)
        self.bottom = random.randint(50, HEIGHT//2 - 50)
        self.x = WIDTH
        self.w = 50
        self.speed = 3

    def show(self):
        screen.blit(pipe_img, (self.x, 0), (0, 0, self.w, self.top))
        screen.blit(pipe_img, (self.x, HEIGHT - self.bottom), (0, 320 - self.bottom, self.w, self.bottom))

    def update(self):
        self.x -= self.speed

bird = Bird()
pipes = []

score = 0

START = 0
PLAYING = 1
GAME_OVER = 2
state = START

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == START or state == GAME_OVER:
                    state = PLAYING
                    bird = Bird()
                    pipes = []
                    score = 0
                    start_sound.play()  
                elif state == PLAYING:
                    bird.up()

    screen.blit(background_img, (0, 0))

    if state == START:
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (WIDTH//2 - 120, HEIGHT//2))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 10))

    elif state == PLAYING:
        bird.update()
        bird.show()

        if len(pipes) == 0 or pipes[-1].x < WIDTH - 150:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.show()
            if pipe.x < -pipe.w:
                pipes.remove(pipe)

            if pipe.x == bird.x:
                score += 1
                if score > high_score:
                    high_score = score

        for pipe in pipes:
            if bird.x + 34 > pipe.x and bird.x < pipe.x + pipe.w:
                if bird.y < pipe.top or bird.y + 24 > HEIGHT - pipe.bottom:
                    state = GAME_OVER
                    game_over_sound.play()  

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif state == GAME_OVER:
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 50))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 50, HEIGHT//2))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH//2 - 70, HEIGHT//2 + 50))
        restart_text = font.render("Press SPACE to Start Over", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - 140, HEIGHT//2 + 100))

    pygame.display.update()
    pygame.time.Clock().tick(60)
