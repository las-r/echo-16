import cpu
import pygame

# echo-16 made by las-r on github
# v0.3

# init pygame
pygame.init()
clock = pygame.time.Clock()

# settings
WIDTH, HEIGHT = 160, 144
SCALE = 4
DWIDTH, DHEIGHT = WIDTH * SCALE, HEIGHT * SCALE

# screen
screen = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("ECHO-16")

# cpu
e16cpu = cpu.e16(screen, WIDTH, HEIGHT, SCALE)
e16cpu.loadRom("test.e16")

# main loop
try:
    run = True
    while run:
        # events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                
        # update screen
        for h, row in enumerate(e16cpu.disp):
            for w, pix in enumerate(row):
                pygame.draw.rect(e16cpu.screen, pix, pygame.Rect(w * SCALE, h * SCALE, SCALE, SCALE))
        pygame.display.flip()
                
        # execute
        for _ in range(int(e16cpu.mhz / 60)):
            e16cpu.step()
        if e16cpu.dt > 0: e16cpu.dt -= 1
        if e16cpu.st > 0: e16cpu.st -= 1
        
        # fps
        clock.tick()
        
# end
except cpu.BreakLoop:
    pass
            
# quit pygame
pygame.quit()
