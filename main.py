import argparse
import cpu
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# echo-16 made by las-r on github
# v0.4

# init pygame
pygame.init()
clock = pygame.time.Clock()

# argument parsing
parser = argparse.ArgumentParser(description="Run the ECHO-16 emulator.")
parser.add_argument("rom", help="Path to the ROM file to load")
parser.add_argument("--beep", default="sounds/beep.wav", help="Path to the beep sound file (default: sounds/beep.wav)")
parser.add_argument("--scale", type=int, default=4, help="Pixel scale factor (default: 4)")
parser.add_argument("--mhz", type=int, default=0.002, help="Clock speed in MHz (default: 0.002)")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

# settings
WIDTH, HEIGHT = 192, 128
SCALE = args.scale
DWIDTH, DHEIGHT = WIDTH * SCALE, HEIGHT * SCALE

# beep sound
beep = pygame.mixer.Sound(args.beep)
beep.set_volume(0.2)

# screen
screen = pygame.display.set_mode((DWIDTH, DHEIGHT))
pygame.display.set_caption("ECHO-16")

# cpu
e16cpu = cpu.e16(screen, WIDTH, HEIGHT, SCALE, args.mhz, args.debug)
e16cpu.loadRom(args.rom)

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
        if e16cpu.st > 0: 
            e16cpu.st -= 1
            beep.play()
        
        # fps
        clock.tick()
        
# end
except cpu.BreakLoop:
    pass
            
# quit pygame
pygame.quit()
