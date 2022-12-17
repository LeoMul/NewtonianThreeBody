import numpy as np

#planet0: S
#planet1: E
#planet2: M

masssun = 333060.402
massmoon = 0.0123031469
# 0  1       2     3      4      5  
#S_x S_y     E_x   E_y    M_x M_y

def calculate_accelerations(positions):
    #assume positions is an np array of size 6
    accelerations = np.zeros(6)

    distanceMSpminus3 = np.sqrt((positions[4] - positions[0])**2 + (positions[5] - positions[1])**2)**(-3)
    distanceESpminus3 = np.sqrt((positions[2] - positions[0])**2 + (positions[3] - positions[1])**2)**(-3)
    distanceEMpminus3 = np.sqrt((positions[2] - positions[4])**2 + (positions[3] - positions[5])**2)**(-3)

    accelerations[0] = distanceESpminus3 * (positions[2]-positions[0]) + (positions[4]-positions[0])*distanceMSpminus3*massmoon
    accelerations[1] = distanceESpminus3 * (positions[3]-positions[1]) + (positions[5]-positions[1])*distanceMSpminus3*massmoon
    accelerations[2] = -distanceESpminus3 * (positions[2]-positions[0])*masssun - distanceEMpminus3 * (positions[2]-positions[4])*massmoon
    accelerations[3] = -distanceESpminus3 * (positions[3]-positions[1])*masssun - distanceEMpminus3 * (positions[3]-positions[5])*massmoon
    accelerations[4] = masssun * distanceMSpminus3 * (positions[0]-positions[4]) + distanceEMpminus3 * (positions[2]-positions[4])
    accelerations[5] = masssun * distanceMSpminus3 * (positions[1]-positions[5]) + distanceEMpminus3 * (positions[3]-positions[5])



    return accelerations

def first_step(initial_positions,initial_velocities,delta_t):
    first_step_int = initial_positions + delta_t*initial_velocities
    first_step_int = first_step_int + calculate_accelerations(initial_positions)
    return first_step_int

def next_verlet(positions,positions_minus_one,delta_t):

    next_verlet_step = 2.0*positions - positions_minus_one + delta_t*delta_t* calculate_accelerations(positions)

    return next_verlet_step 