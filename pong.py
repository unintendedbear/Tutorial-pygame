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

# Path for the background image
ball_path = "images/ball.png"

# Ball object
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(ball_path, True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 # Ball will appear in the center of the background
        self.rect.centery = HEIGHT / 2
        self.speed = [0.5, -0.5]

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

    background = load_image(backgrnd_path, False)

    ball = Ball()

    # Maintains screen opened unless manually closed
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(ball.image, ball.rect)
        pygame.display.flip()
    return 0

# Initialise pygame
if __name__ == '__main__':
    pygame.init()
    main()
