# import the pygame module
# import sys module for exiting the window
import pygame

# import some useful constants
from pygame.locals import *

# initialise the pygame module
pygame.init()

# create a new drawing suftace, width=300, height=300
DISPLAYSURF = pygame.display.set_mode((300,300))
# caption window
pygame.display.set_caption('My First Game')

# loop forever
while True:

    # get user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end game and close window
            pygame.quit()
            sys.exit()

    # update the display
    pygame.display.update()
