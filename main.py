import cpu
import pygame

# echo-16 made by las-r on github
# v0.1

# init pygame
pygame.init()

# settings
WIDTH, HEIGHT = 160, 144
SCALE = 4
DWIDTH, DHEIGHT = WIDTH * SCALE, HEIGHT * SCALE

# display
disp = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
screen = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("ECHO-16")

# main loop
run = True
while run:
    # events
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            run = False
            
# quit pygame
pygame.quit()
