#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""example1.py"""

# Import pygame
import pygame
from pygame.locals import *
import sys

# Window width and height, they'll be constants for now
WIDTH = 640
HEIGHT = 480

# Path for the background image
backgrnd_path = "images/background_pong.png"

# Paths for the ball and the paddle images
ball_path = "images/ball.png"
paddle_path = "images/paddle.png"

# Ball object
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(ball_path, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 # Ball will appear in the center of the background
        self.rect.centery = HEIGHT / 2
        self.speed = [0.5, -0.5]

    # Controling ball movement
    def refresh(self, time, paddle_player):
        self.rect.centerx += self.speed[0] * time # Basic physics
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, paddle_player):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

# Paddle object
class Paddle(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(paddle_path, False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x # Paddle will move over the y axis
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def move(self, time, pressed_key):
        if self.rect.top >= 0 and pressed_key[K_UP]:
            self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT and pressed_key[K_DOWN]:
            self.rect.centery += self.speed * time

# Function which loads an image into the Window
def load_image(path, transparent):
    try: image = pygame.image.load(path)
    # Manages error if image cannot be loaded
    except pygame.error, message:
        raise SystemExit, message
    # Converting to inner pygame format (more efficient)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image


# Define main
def main():
    # Creating screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Unintended Pong")

    # Graphic elements
    background = load_image(backgrnd_path, False)
    ball = Ball()
    paddle_player = Paddle(20)

    # Creating clock so the ball moves
    clock = pygame.time.Clock()

    # Maintains screen opened unless manually closed
    while True:
        time = clock.tick(60)
        # Whic key is pressed?
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        ball.refresh(time, paddle_player)
        paddle_player.move(time, pressed_key)
        screen.blit(background, (0, 0))
        screen.blit(ball.image, ball.rect)
        screen.blit(paddle_player.image, paddle_player.rect)
        pygame.display.flip()
    return 0

# Initialise pygame
if __name__ == '__main__':
    pygame.init()
    main()
