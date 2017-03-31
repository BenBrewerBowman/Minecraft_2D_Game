# Author: Ben Brewer
# Date created: March 31, 2017

# import the pygame module
# import sys module for exiting the window
import pygame
import random
# import some useful constants
from pygame.locals import *

# GAME MAP DIMENSIONS
# num pixels per tile
TILESIZE = 40
# num tiles wide and high
MAPWIDTH  = 10
MAPHEIGHT = 10

# constants representing colors
BLACK = (0,0,0)

# constants representing resources
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5

# constants representing rarity
BASE_RARITY = 0
VERY_COMMON = 30
COMMON      = 45
RARE        = 50
VERY_RARE   = 53
ULTRA_RARE  = 54

# list of resources
resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA]

# dictionary(hash) linking resources to textures
textures = {
    DIRT  : pygame.image.load('Images/DirtPixel.png'),
    GRASS : pygame.image.load('Images/GrassPixel.png'),
    WATER : pygame.image.load('Images/WaterPixel.png'),
    COAL  : pygame.image.load('Images/CoalPixel.png'),
    ROCK  : pygame.image.load('Images/RockPixel.png'),
    LAVA  : pygame.image.load('Images/LavaPixel.png')
}


# initialize pygame module
pygame.init()
# create new drawing suftace, mapwidth, mapheight
DISPLAY_SURFACE = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
# caption window
pygame.display.set_caption('Minecraft 2D')

# randomly generate resources for map based on rarity of each resource
tilemap = [ [GRASS for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)]
for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
        random_num = random.randint(BASE_RARITY, ULTRA_RARE)
        # very common resource
        if random_num < VERY_COMMON:
            if (random_num % 3) == 0:
                this_tile = ROCK
            else:
                this_tile = GRASS
        # common resource
        if random_num >= VERY_COMMON and random_num < COMMON:
            if (random_num % 2) == 0:
                this_tile = WATER
            else:
                this_tile = DIRT
        # rare resource
        if random_num >= RARE and random_num < VERY_RARE:
            if (random_num % 2) == 0:
                this_tile = COAL
            else:
                this_tile = LAVA
        # ultra rare resource
        #   GOES HERE
        # save tile to map
        tilemap[row][column] = this_tile


inventory = {
    DIRT  : 0
    GRASS : 0
    WATER : 0
    COAL  : 0
    ROCK  : 0
}

# the player
PLAYER = pygame.image.load('Images/Megaman_Player.gif')
# randomly place the player (initially)
player_position = [random.randint(0, MAPWIDTH), random.randint(0, MAPHEIGHT)]

# game loop
while True:

    # get user events
    for event in pygame.event.get():
        # print(event)
        # if the user wants to quit
        if event.type == QUIT:
            # end game and close window
            pygame.quit()
            sys.exit()
        # user presses a key down
        elif event.type == KEYDOWN:
            # right arrow key
            if (event.key == K_RIGHT) and (player_position[0] < MAPWIDTH - 1):
                # player move right
                player_position[0] +=1
            # left arrow key
            elif (event.key == K_LEFT) and (player_position[0] > 0):
                # player move left
                player_position[0] -=1
            # up arrow key
            elif (event.key == K_UP) and (player_position[1] > 0):
                # player move up
                player_position[1] -=1
            # down arrow key
            elif (event.key == K_DOWN) and (player_position[1] < MAPHEIGHT - 1):
                # player move down
                player_position[1] +=1


    # loop through each row
    for row in range(MAPHEIGHT):
        # loop through each column
        for column in range(MAPWIDTH):
            # draw color(RGB) and (x, y, width, height)
            DISPLAY_SURFACE.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

    # display player at correct location
    DISPLAY_SURFACE.blit(PLAYER, (player_position[0]*TILESIZE, player_position[1]*TILESIZE))
    # update the display
    pygame.display.update()
