import pygame 
from pygame.locals import *
import sys 

def render():
    pygame.draw.circle(screen,BLACK,origin,10)


w,h = 800,480
origin = (w/2,h/2)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,255,0)

screen = pygame.display.set_mode((w,h))
screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  
    clock.tick(60)
    pygame.display.update()
    render()