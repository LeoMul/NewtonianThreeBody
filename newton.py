import numpy as np
import pygame 
from pygame.locals import *
import sys 

#planet0: S
#planet1: E
#planet2: M

masssun = 330000
massmoon = 0.0123031469
# 0  1       2     3      4      5  
#S_x S_y     E_x   E_y    M_x M_y

def calculate_accelerations(positions):
    #assume positions is an np array of size 6
    accelerations = np.zeros(6)

    distanceMS = np.sqrt((positions[4] - positions[0])**2 + (positions[5] - positions[1])**2)
    distanceES = np.sqrt((positions[2] - positions[0])**2 + (positions[3] - positions[1])**2)
    distanceEM = np.sqrt((positions[2] - positions[4])**2 + (positions[3] - positions[5])**2)



    distanceMSpminus3 = distanceMS**(-3)
    distanceESpminus3 = distanceES**(-3)
    distanceEMpminus3 = distanceEM**(-3)
    #print("Positions:")
    #print(positions)
    #print("distances to power -3")
    #print(distanceMSpminus3,distanceESpminus3,distanceEMpminus3)

    accelerations[0] = - distanceESpminus3 * (positions[0]-positions[2]) - (positions[0]-positions[4])*distanceMSpminus3*massmoon
    accelerations[1] = - distanceESpminus3 * (positions[1]-positions[3]) - (positions[1]-positions[5])*distanceMSpminus3*massmoon
    
    accelerations[2] = - distanceESpminus3 * (positions[2]-positions[0])*masssun - distanceEMpminus3 * (positions[2]-positions[4])*massmoon
    accelerations[3] = - distanceESpminus3 * (positions[3]-positions[1])*masssun - distanceEMpminus3 * (positions[3]-positions[5])*massmoon
    
    accelerations[4] = - distanceMSpminus3 * (positions[4]-positions[0])*masssun - distanceEMpminus3 * (positions[4]-positions[2])
    accelerations[5] = - distanceMSpminus3 * (positions[5]-positions[1])*masssun -  distanceEMpminus3 * (positions[5]-positions[3])

    
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
    scale = 200
    moonscale = 50.0
    x_s = w/2 + scale*positions[0]
    y_s = h/2 + scale*positions[1]

    x_e = w/2 + scale*positions[2]
    y_e = h/2 + scale*positions[3]
    #x_m = w/2 + scale*positions[4]
    #y_m = h/2 + scale*positions[5]
    #the orbit of the moon kind of sucks so we have to amplify it
    x_m = x_e + moonscale*scale*(positions[4]-positions[2])
    y_m = y_e + moonscale*scale*(positions[5]-positions[3])


    pygame.draw.circle(screen,BLACK,(x_s,y_s),20)
    pygame.draw.circle(screen,RED,(x_e,y_e),10)
    pygame.draw.circle(screen,BLUE,(x_m,y_m),5)


w,h = 1400,700
origin = (w/2,h/2)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

screen = pygame.display.set_mode((w,h))
screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()

positions = np.array([0,0,1.0,0.0,1.0,0.002569])
delta_t = 1.0e-5
initial_velocities = np.array([0.0,0.0,0.0,np.sqrt(masssun),np.sqrt(masssun)/30.0,np.sqrt(masssun)])

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