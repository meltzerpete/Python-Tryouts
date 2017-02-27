import os
import sys
from random import randint

def print_currrent_state(x):
    for row in range(12):
        for col in range(30):
            print(x[30 * row + col], end='')
        print("")
    print("")

def hop_fire(a, x):
    """
    Hopfield firing function where a is the energy abd x is the current state
    """
    if a > 0:
        return 1
    elif a < 0:
        return 0
    else:
        return x

# Read patterns from file
counter = 0
patterns = []
current = []

for filename in os.listdir('./StoredPatterns'):

     with open('./StoredPatterns/' + filename) as f:
         while True:
             c = f.read(1)
             if not c:
                 counter += 1
                 #print("End of file ", counter)
                 patterns.append(current)
                 current = []
                 break
             if c == '\n':
                 pass
                 #print("newline")
             else:
                 current.append(int(c))
                 #print("Read a character: %s" % c)

# print(patterns)

# 1. Assign connection weights
# ============================

# Initialise weights arrays
n_nodes = 360
weights = [[0 for i in range(n_nodes)] for j in range(n_nodes)]

for i in range(n_nodes):
    # for each node calculate all weights
    for j in range(n_nodes):
        if i == j:
            weights[i][j] = 0
        else:
            # calculate weight w_ij
            sum = 0
            for pattern in patterns:
                # for each pattern
                sum += (2 * pattern[i] - 1) * (2 * pattern[j] - 1)
            weights[i][j] = sum

# print(weights)


# 2. Initialise with unkown pattern
# =================================
state = []

# read starting state from file
with open(sys.argv[1]) as f:
    while True:
        c = f.read(1)
        if not c:
            #print("End of file ", counter)
            break
        if c == '\n':
            pass
            #print("newline")
        else:
            state.append(int(c))
            #print("Read a character: %s" % c)

assert len(state) == n_nodes


# 3. Iterate until convergence
# ============================

breaker = 0;

while breaker < 1000:
    # print current state
    print_currrent_state(state)

    # Pick node at random
    i = randint(0, n_nodes - 1)

    # calculate energy
    energy = 0
    for j in range(n_nodes):
        if i != j:
            energy += weights[i][j] * state[j]

    # update ith node
    new_state = hop_fire(energy, state[i])

    # check for convergence and update ith node
    if state[i] == new_state:
        breaker += 1
    else:
        breaker = 0
        state[i] = new_state
