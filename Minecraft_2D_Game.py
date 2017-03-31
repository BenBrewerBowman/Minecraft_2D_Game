# import the pygame module
# import sys module for exiting the window
import pygame
import random
# import some useful constants
from pygame.locals import *

# game map dimensions
TILESIZE = 40
MAPWIDTH  = 3
MAPHEIGHT = 6

# constants representing colors
BLACK = (0,0,0)

# constants representing resources
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5
# list of resources
resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA]

# dictionary linking resources to textures
textures = {
    DIRT  : pygame.image.load('DirtPixel.png'),
    GRASS : pygame.image.load('GrassPixel.png'),
    WATER : pygame.image.load('WaterPixel.png'),
    COAL  : pygame.image.load('CoalPixel.png'),
    ROCK  : pygame.image.load('RockPixel.png'),
    LAVA  : pygame.image.load('LavaPixel.png')
}

tilemap = [ [random.choice(resources) for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)]

# initialise the pygame module
pygame.init()
# create a new drawing suftace, width, height
DISPLAY_SURFACE = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
# caption window
pygame.display.set_caption('Minecraft 2D')

# game loop
while True:

    # get user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end game and close window
            pygame.quit()
            sys.exit()

    # loop through each row
    for row in range(MAPHEIGHT):
        # loop through each column
        for column in range(MAPWIDTH):
            # draw color(RGB) and (x, y, width, height)
            DISPLAY_SURFACE.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

    # update the display
    pygame.display.update()
