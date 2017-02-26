import os, curses, time
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
    # draw vertical separator
    stdscr.addch(0, 34, '\u252c')
    for i in range(1, curses.LINES - 1):
        stdscr.addch(i, 34, '\u2502')
    stdscr.addch(curses.LINES - 1, 34, '\u2534')

    # turn off cursor
    curses.curs_set(False)

    # display messages
    stdscr.addstr(16, 2, "Press 's' to start.")
    stdscr.addstr(18, 2, "Press 'q' to quit.")

    stdscr.addstr(2, 36, "Select input file ( \u2bc5 / \u2bc6 ):")

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


    # display files in Inputs directory

    start_row = 4
    inc = 0
    files = []
    for filename in os.listdir('./Inputs'):
        files.append("./Inputs/" + filename)
        stdscr.addstr(start_row + inc, 38, str(inc + 1) + ". " + filename)
        inc += 1

    selection = 0
    stdscr.addch(4, 36, '\u2b62')
    # loop while selecting input - s triggers start
    key = '1'
    while True:

        # don't check keypress for first run
        if key != '1':
            key = stdscr.getch()
        else:
            key = ''

        if key == ord('s'):
            # 3. Iterate until convergence
            # ============================

            breaker = 0;

            # turn off cursor
            curses.curs_set(True)

            # variables for flow control
            loop = 0
            nbreaker = 0
            old_total_energy = 0

            while nbreaker < 100:
                # Pick node at random
                i = randint(0, n_nodes - 1)

                # calculate energy
                energy = 0
                for j in range(n_nodes):
                    if i != j:
                        energy += weights[i][j] * state[j]

                # calculate total energy - every 10 loops for performance
                if loop == 0:
                    total_energy = 0
                    for n in range(len(weights)):
                        for m in range(n + 1, len(weights[n])):
                            total_energy += weights[n][m] * state[n] * state[m]

                    total_energy = -1 * total_energy

                    # display currrent total energy
                    curses.curs_set(False)
                    stdscr.addstr(20, 2, "Current energy:" + str(total_energy))
                    curses.curs_set(True)

                    # check for convergence
                    if total_energy == old_total_energy:
                        nbreaker += 1
                    else:
                        nbreaker = 0
                    old_total_energy = total_energy

                loop = (loop + 1) % 10

                # update ith node
                state[i] = hop_fire(energy, state[i])

                # display change
                if state[i] == 1:
                    stdscr.addch(2 + i // 30, 2 + i % 30, '\u2593')
                else:
                    stdscr.addch(2 + i // 30, 2 + i % 30, '\u2591')


                stdscr.refresh()
                # slow me down!!
                time.sleep(0.001)

            # finished
            curses.curs_set(False)
            stdscr.addstr(22, 2, "Finished! Press any key..")

            while True:
                exit_key = stdscr.getch()
                stdscr.addstr(20, 2, "                         ")
                stdscr.addstr(22, 2, "                         ")
                if exit_key == ord('q'):
                    exit()
                break

        stdscr.refresh()

        if key == ord('q'):
            return

        if key == curses.KEY_UP:
            selection = max(0, selection - 1)

        if key == curses.KEY_DOWN:
            selection = min(len(files) - 1, selection + 1)

        # display selection
        start_row = 4
        for i in range(len(files)):
            if (i == selection):
                stdscr.addch(start_row + i, 36, '\u2b62')
            else:
                stdscr.addch(start_row + i, 36, ' ')

        # 2. Initialise with unkown pattern
        # =================================
        state = []

        # read starting state from file
        with open(files[selection]) as f:
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

curses.wrapper(main)
