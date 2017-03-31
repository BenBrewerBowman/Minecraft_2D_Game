# Author: Ben Brewer
# Date created: March 31, 2017

# import the pygame module
# import sys module for exiting the window
import pygame
import random
# import some useful constants
from pygame.locals import *

# frames per second clock (cloud transitions)
fpsClock = pygame.time.Clock()

# GAME MAP DIMENSIONS
# num pixels per tile
TILESIZE = 40
# num tiles wide and high
MAPWIDTH  = 20
MAPHEIGHT = 20
# num pixels for inventory screen size
INVHEIGHT = 2*TILESIZE
PADDING = TILESIZE/2

# constants representing colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# CONSTANTS REPRESENTING OBJECTS
# resources
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5
WOOD  = 6
FIRE  = 7
SAND  = 8
STONE = 9
BRICK = 10
# objects that are NOT resources
CLOUD = 11

# list of resources
resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA, WOOD, FIRE, SAND, STONE, BRICK]

# dictionary(hash) linking resources to textures
textures = {
    DIRT  : pygame.image.load('Images/DirtPixel.png'),
    GRASS : pygame.image.load('Images/GrassPixel.png'),
    WATER : pygame.image.load('Images/WaterPixel.png'),
    COAL  : pygame.image.load('Images/CoalPixel.png'),
    ROCK  : pygame.image.load('Images/RockPixel.png'),
    LAVA  : pygame.image.load('Images/LavaPixel.png'),
    WOOD  : pygame.image.load('Images/WoodPixel.png'),
    FIRE  : pygame.image.load('Images/TorchPixel.png'),
    SAND  : pygame.image.load('Images/SandPixel.png'),
    STONE : pygame.image.load('Images/StonePixel.png'),
    BRICK : pygame.image.load('Images/BrickPixel.png'),
    CLOUD : pygame.image.load('Images/CloudPixel.png')
}

# player resource inventory
inventory = {
    DIRT  : 0,
    GRASS : 0,
    WATER : 0,
    COAL  : 0,
    ROCK  : 0,
    LAVA  : 0,
    WOOD  : 0,
    FIRE  : 0,
    SAND  : 0,
    STONE : 0,
    BRICK : 0
}

# recipes for crafting new resources
craft = {
    WOOD  : { DIRT:  2},
    FIRE  : { WOOD:  2,  COAL: 1},
    SAND  : { DIRT:  1,  ROCK: 1},
    STONE : { ROCK:  2},
    BRICK : { STONE: 1,  SAND: 1}
}

# maps each resource to number event keys used to place/craft the resource
controls = {
    DIRT  : 49,     # event 49 is 1 key
    GRASS : 50,     # event 50 is 2 key
    WATER : 51,     # event 51 is 3 key
    COAL  : 52,     # event 52 is 4 key
    ROCK  : 53,     # event 53 is 5 key
    LAVA  : 54,     # event 54 is 6 key
    WOOD  : 55,     # event 54 is 7 key
    FIRE  : 56,     # event 55 is 8 key
    SAND  : 57,     # event 56 is 9 key
    STONE : 48,     # event 57 is 0 key
    BRICK : 45      # event 49 is - key
}

# CONSTANTS REPRESENTING RARITY
BASE_RARITY = 0
VERY_COMMON = 30
COMMON      = 45
RARE        = 50
VERY_RARE   = 53
ULTRA_RARE  = 54

# initialize pygame module
pygame.init()
# create new drawing suftace, mapwidth, mapheight
DISPLAY_SURFACE = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + INVHEIGHT))
# caption window
pygame.display.set_caption('M I N E C R A F T -- 2 D')

pygame.display.set_icon(pygame.image.load('Images/Megaman_Player.gif'))

# RANDOMLY GENERATE RESOURCES FOR MAP BASED ON RARITY
tilemap = [ [GRASS for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)]
for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
        random_num = random.randint(BASE_RARITY, ULTRA_RARE)
        this_tile = GRASS
        # very common resource
        if random_num < VERY_COMMON:
            if (random_num % 3) == 0:
                this_tile = ROCK
            else:
                this_tile = GRASS
        # common resource
        elif random_num >= VERY_COMMON and random_num < COMMON:
            if (random_num % 2) == 0:
                this_tile = WATER
            else:
                this_tile = DIRT
        # rare resource
        elif random_num >= RARE and random_num < VERY_RARE:
            if (random_num % 2) == 0:
                this_tile = COAL
            else:
                this_tile = LAVA
        # ultra rare resource
        #   GOES HERE
        # save tile to map
        tilemap[row][column] = this_tile

# load font style and size
INVFONT = pygame.font.Font('Fonts/freesansbold.ttf', 18)

# PLAYER
PLAYER = pygame.image.load('Images/Megaman_Player.gif')
# randomly place the player (initially)
player_position = [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)]

#CLOUD POSITION
# fixed x offscreen
cloud_x_pos = [-200, -500, -1000]
# random y pos
cloud_y_pos = [random.randint(0, MAPHEIGHT*TILESIZE - 1), random.randint(0, MAPHEIGHT*TILESIZE - 1), random.randint(0, MAPHEIGHT*TILESIZE - 1)]


# GAME LOOP
while True:
    # clear screen
    DISPLAY_SURFACE.fill(BLACK)

    # EVENTS
    # get user events
    for event in pygame.event.get():
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
            # space bar key
            elif (event.key == K_SPACE):
                # tile player is standing on
                this_tile = tilemap[player_position[1]][player_position[0]]
                # add resource to inventory
                inventory[this_tile] +=1
                # player is now standing on dirt
                tilemap[player_position[1]][player_position[0]] = DIRT

            # PLACE RESOURCES FROM INVENTORY. SWAP WITH RESOURCE WHERE PLAYER STANDING
            for key in controls:
                # place/craft item key pressed
                if (event.key == controls[key]):
                    # if craft key pressed
                    if key in craft:
                        # initialize to true
                        canBeMade = True
                        # check to see if there are enough resources in inventory to craft item
                        for each in craft[key]:
                            # if not enough resources in inventory
                            if craft[key][each] > inventory[each]:
                                # cannot craft item
                                canBeMade = False
                        # if enought available resources, craft item
                        if canBeMade == True:
                            # remove each ingredient from craft recipe
                            for i in craft[key]:
                                inventory[i] -= craft[key][i]
                            # add crafted item to inventory
                            inventory[key] += 1
                    # place item of key pressed
                    else:
                        # if there is at least one item in inventory
                        if inventory[key] > 0:
                            # get tile to swap with item
                            standing_tile = tilemap[player_position[1]][player_position[0]]
                            # increase inventory by standing tile
                            inventory[standing_tile] += 1
                            # remove item to place from inventory
                            inventory[key] -= 1
                            # place item from inventory
                            tilemap[player_position[1]][player_position[0]] = key

    # DISPLAY UPDATED MAP
    # loop through each row
    for row in range(MAPHEIGHT):
        # loop through each column
        for column in range(MAPWIDTH):
            # draw color(RGB) and (x, y, width, height)
            DISPLAY_SURFACE.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

    # DISPLAY INVENTORY
    # set inventory positions on screen
    inventory_x_position = PADDING
    inventory_y_position = MAPHEIGHT*TILESIZE + PADDING
    # for each inventory item available
    for item in resources:
        # add image of resource
        DISPLAY_SURFACE.blit(textures[item], (inventory_x_position, inventory_y_position))
        # padding for text
        inventory_x_position += PADDING
        # add txt amt in inventory and display it
        numInventoryText = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAY_SURFACE.blit(numInventoryText, (inventory_x_position, inventory_y_position))
        # padding between resources
        inventory_x_position += PADDING*2

    # DISPLAY PLAYER AT LOCATION
    DISPLAY_SURFACE.blit(PLAYER, (player_position[0]*TILESIZE, player_position[1]*TILESIZE))

    # DISPLAY CLOUDS
    # display each instance of a cloud
    for each in range(len(cloud_x_pos)):
        # display cloud on screen
        DISPLAY_SURFACE.blit(textures[CLOUD], (cloud_x_pos[each], cloud_y_pos[each]))
        # move cloud to right slightly
        cloud_x_pos[each] += 1
        # once cloud moves to end of map
        if cloud_x_pos[each] > MAPWIDTH*TILESIZE:
            # randomly pick a new position to place the cloud (clouds in random frequency and position)
            # random x distance offscreen
            cloud_x_pos[each] = -random.randint(0, 450)
            # random y pos
            cloud_y_pos[each] = random.randint(0, MAPHEIGHT*TILESIZE - 1)

    # UPDATE WINDOW
    pygame.display.update()
    fpsClock.tick(24)

#END WHILE LOOP
