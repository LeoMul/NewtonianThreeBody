import numpy as np
import pygame 
from pygame.locals import *
import sys 

#planet0: S
#planet1: E
#planet2: M

masssun = 3
# 0  1       2     3      4      5  
#S_x S_y     E_x   E_y    M_x M_y

def calculate_accelerations(positions):
    #assume positions is an np array of size 4
    accelerations = np.zeros(4)

    distanceES = np.sqrt((positions[2] - positions[0])**2 + (positions[3] - positions[1])**2)



    distanceESpminus3 = distanceES**(-3)
    #print("Positions:")
    #print(positions)
    #print("distances to power -3")
    #print(distanceMSpminus3,distanceESpminus3,distanceEMpminus3)

    accelerations[0] = - distanceESpminus3 * (positions[0]-positions[2]) 
    accelerations[1] = - distanceESpminus3 * (positions[1]-positions[3]) 
    
    accelerations[2] = -distanceESpminus3 * (positions[2]-positions[0])*masssun 
    accelerations[3] = -distanceESpminus3 * (positions[3]-positions[1])*masssun 
     
    #print(accelerations)

    return accelerations

def first_step(initial_positions,initial_velocities,delta_t):
    first_step_int = initial_positions + delta_t*initial_velocities
    first_step_int = first_step_int + 0.5*delta_t*delta_t*calculate_accelerations(initial_positions)
    print(first_step_int)
    return first_step_int

def next_verlet(positions,positions_minus_one,delta_t):
    acceleration = calculate_accelerations(positions)
    #print(acceleration)
    next_verlet_step = 2.0*positions - positions_minus_one + delta_t*delta_t*acceleration
    #print(next_verlet_step)
    return next_verlet_step 

def render(positions):
    screen.fill(WHITE)
    scale = 50

    x_s = w/2 + scale*positions[0]
    y_s = h/2 + scale*positions[1]

    x_e = w/2 + scale*positions[2]
    y_e = h/2 + scale*positions[3]

    pygame.draw.circle(screen,BLACK,(x_s,y_s),10)
    pygame.draw.circle(screen,RED,(x_e,y_e),10)


w,h = 800,480
origin = (w/2,h/2)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

screen = pygame.display.set_mode((w,h))
screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()

positions = np.array([0,0,1,0])
delta_t = 1.0e-3
initial_velocities = np.array([0.0,0.0,0.0,np.sqrt(masssun)])

positions_minus_one = positions
positions = first_step(positions_minus_one,initial_velocities,delta_t)

i = 0
max_index = 1e+8#
while i < max_index: 
    i+= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  
    clock.tick(60)
    pygame.display.update()

    #updating the positions.
    new_positions = next_verlet(positions,positions_minus_one,delta_t)

    positions_minus_one = positions
    positions = new_positions

    print(positions)

    render(new_positions)