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

# Define main
def main():
    # Creating screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Testing testing!")
    # Maintains screen opened unless manually closed
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
    return 0

# Initialise pygame
if __name__ == '__main__':
    pygame.init()
    main()
