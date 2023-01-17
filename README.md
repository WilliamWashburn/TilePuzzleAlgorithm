This repository is my practice to learn about algorithms while reading "Planning Algorithms" by Steven M. LaValle.

To practice, I am writing a program to solve the "sliding puzzle" game: https://en.wikipedia.org/wiki/Sliding_puzzle

We are considering an N by N puzzle. For now, N = 3
For a 3 by 3 puzzle, there is a 3 by 3 grid of tiles with 1 tile missing. We can represent the tiles like this:
    
    [ 0 1 2
      3 4 5
      6 7 8 ]
We will consider the 0 to represent the missing tile.

## State 
We are defining the puzzle by a list of numbers representing the tile order. [3, 4, 7, 2, 8, 6, 1, 0, 5]

## State Space
The state space is any unique arrangment of these tiles. This is finite and there are (N*N)! possible states or 362880 for N = 3

## Goal State
[1, 2, 3, 4, 5, 6, 7, 8, 0]

## Transition Function
When a tile is moved, it has to be adjacent to the missing tile (0).
In general, there are 4 movements,
1. The right tile moves to fill in the space
2. the left tile moves to fill in the space
3. the top tile moves to fill in the space
4. the bottom tile moves to fill in the space
If the blank tile is on the edge of the board, then there is only 3 possible movements
If the blank tile is in the corner of the board, then there is only 2 possible movements

This is explained more throughly here: [a relative link](appendix/movementDefinitions.md)