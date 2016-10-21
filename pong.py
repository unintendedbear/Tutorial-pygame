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

# Path for the fonts
font_path = "images/telegrama_raw.otf"

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
    def refresh(self, time, paddle_player, paddle_CPU, points):
        self.rect.centerx += self.speed[0] * time # Basic physics
        self.rect.centery += self.speed[1] * time
        # Losing or gaining points
        if self.rect.left <= 0:
            points[1] += 1
        if self.rect.right >= WIDTH:
            points[0] += 1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        # Avoiding collision with the paddles
        if pygame.sprite.collide_rect(self, paddle_player) or pygame.sprite.collide_rect(self, paddle_CPU):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        return points

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

    def ia(self, time, ball):
        # As CPU: "Is the ball on my side of the table and moving towards me?"
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            else:
                self.rect.centery -= self.speed * time

# Function which loads an image into the Window
def load_image(path, transparent):
    try: image = pygame.image.load(path)
    # Manages error if image cannot be loaded
    except (pygame.error) as message:
        raise(message)
    # Converting to inner pygame format (more efficient)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

# Function to manage texts
def text(text, posx, posy, color):
    font = pygame.font.Font(font_path, 25)
    output = pygame.font.Font.render(font, text, 1, color) # Transforms font into a Sprite
    output_rect = output.get_rect()
    output_rect.centerx = posx
    output_rect.centery = posy

    return output, output_rect


# Define main
def main():
    # Creating screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Unintended Pong")

    # Graphic elements
    background = load_image(backgrnd_path, False)
    ball = Ball()
    paddle_player = Paddle(10)
    paddle_CPU = Paddle(WIDTH - 10)
    paddle_CPU.speed = 0.45

    # Creating clock so the ball moves
    clock = pygame.time.Clock()

    # Scoring initialisation
    points = [0, 0]

    # Maintains screen opened unless manually closed
    while True:
        time = clock.tick(60)
        # Whic key is pressed?
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        points = ball.refresh(time, paddle_player, paddle_CPU, points)
        paddle_player.move(time, pressed_key)
        paddle_CPU.ia(time, ball)

        # Showing scores
        font_color = (0, 0, 0)
        score_player, score_player_rect = text(str(points[0]), WIDTH/4, 40, font_color)
        score_CPU, score_CPU_rect = text(str(points[1]), WIDTH-WIDTH/4, 40, font_color)

        screen.blit(background, (0, 0))
        screen.blit(ball.image, ball.rect)
        screen.blit(paddle_player.image, paddle_player.rect)
        screen.blit(score_player, score_player_rect)
        screen.blit(paddle_CPU.image, paddle_CPU.rect)
        screen.blit(score_CPU, score_CPU_rect)
        pygame.display.flip()
    return 0

# Initialise pygame
if __name__ == '__main__':
    pygame.init()
    main()
