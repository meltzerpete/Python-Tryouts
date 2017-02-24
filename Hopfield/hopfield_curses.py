import os, sys, curses, time
from random import randint

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

def main(stdscr):
    # set up display
    stdscr.clear()
    stdscr.border(0)

    # turn off cursor
    curses.curs_set(False)

    # display message
    stdscr.addstr(2, 40, "Press 's' to start.")
    stdscr.addstr(3, 40, "Press 'q' to quit.")

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

    # display starting state
    current = 0
    for i in range(12):
        for j in range(30):
            if state[current] == 1:
                stdscr.addch(2 + i, 2 + j, '\u2593')
            else:
                stdscr.addch(2 + i, 2 + j, '\u2591')
            current += 1

    # update display and pause until user signals start
    stdscr.refresh()
    key = ''
    while key != ord('s'):
        if key == ord('q'):
            return
        key = stdscr.getch()

    # 3. Iterate until convergence
    # ============================

    breaker = 0;

    # turn off cursor
    curses.curs_set(True)

    while breaker < 4 * n_nodes:
        # Pick node at random
        i = randint(0, n_nodes - 1)

        # calculate energy
        energy = 0
        for j in range(n_nodes):
            if i != j:
                energy += weights[i][j] * state[j]

        # update ith node
        new_state = hop_fire(energy, state[i])

        # display change
        if new_state == 1:
            stdscr.addch(2 + i // 30, 2 + i % 30, '\u2593')
        else:
            stdscr.addch(2 + i // 30, 2 + i % 30, '\u2591')

        stdscr.refresh()
        time.sleep(0.001)


        # check for convergence and update ith node
        if state[i] == new_state:
            breaker += 1
        else:
            breaker = 0
            state[i] = new_state

    # finished
    curses.curs_set(False)
    stdscr.addstr(10, 40, "Finished!")

    key = ''
    while key != ord('q'):
        key = stdscr.getch()

if len(sys.argv) <= 1:
    print("\nYou must enter a starting pattern file as a command line argument.")
    print("i.e. $ python3 hopfield_curses.py start1\n")
    exit()

curses.wrapper(main)
