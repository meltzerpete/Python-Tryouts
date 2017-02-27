Implementation of Hopfield Network with Curses UI
=================================================

To run type: `python3 hopfield\_curses.py` at the terminal.

All patterns stored in the 'StoredPatterns' folder will be loaded and stored in the weights.

All patterns stored in the 'Inputs' folder will be accessible from within the application as starting states for the network.

Iteration stops when convergence is percieved, not necessarily when the output matches a stored pattern (due to the non-deterministic behaviour of the network).

Due to the use of 0 thesholds, the inverses of desired pattern to be stored are also stored, this is evident in some of the sample input states.
