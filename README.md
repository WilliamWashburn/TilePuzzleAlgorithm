**Definitions**
We are considering an N by N puzzle. For now, N = 3
For a 3 by 3 puzzle, there is a 3 by 3 grid of tiles with 1 tile missing.
    [ 0 1 2
      3 4 5
      6 7 8 ]
We will consider the 0 to represent the missing tile.

## State 
We are defining the puzzle by a list of numbers representing the tile order. [3, 4, 7, 2, 8, 6, 1, 0, 5]

## State Space
The state space is any unique arrangment of these tiles. This is finite and there are 3!9 possible states.

## Goal State
[1, 2, 3, 4, 5, 6, 7, 8, 0]

## Transition Function
When a tile is moved, it has to be adjacent to the missing tile (0).
In general, there are 4 movements,
1. The right tile moves to fill in the space
2. the left tile moves
3. the top tile moves
4. the bottom tile moves
If the blank tile is on the edge of the board, then there is only 3 possible movements
If the blank tile is in the corner of the board, then there is only 2 possible movements

### Right move
Lets assume that the state is 
[3, 4, 7, 2, 8, 6, 1, 0, 5] or graphically,
[3, 4, 7,
 2, 8, 6,
 1, 0, 5]

 A right move would give,
 [3, 4, 7,
 2, 8, 6,
 1, 5, 0] or
 [3, 4, 7, 2, 8, 6, 1, 5, 0]

given that 0 is index 7, we swap x[7] <=> x[8] or 
x[i] <=> x[i+1] where i is the index of 0

### Left move
Lets assume that the state is 
[3, 4, 7, 2, 8, 6, 1, 0, 5] or graphically,
[3, 4, 7,
 2, 8, 6,
 1, 0, 5]

 A left move would give,
 [3, 4, 7,
  2, 8, 6,
  0, 1, 5] or
 [3, 4, 7, 2, 8, 6, 0, 1, 5]

given that 0 is index 7, we swap x[7] <=> x[6] or 
x[i] <=> x[i-1] where i is the index of 0

### Top move
Lets assume that the state is 
[3, 4, 7, 2, 0, 6, 1, 8, 5] or graphically,
[3, 4, 7,
 2, 0, 6,
 1, 8, 5]

 A top move would give,
 [3, 0, 7,
  2, 4, 6,
  1, 8, 5] or
 [3, 0, 7, 2, 4, 6, 1, 8, 5]

given that 0 is index 4, we swap x[4] <=> x[1] or 
x[i] <=> x[i-N] where i is the index of 0

### Bottom move
Lets assume that the state is 
[3, 4, 7, 2, 0, 6, 1, 8, 5] or graphically,
[3, 4, 7,
 2, 0, 6,
 1, 8, 5]

 A top move would give,
 [3, 4, 7,
  2, 8, 6,
  1, 0, 5] or
 [3, 4, 7, 2, 8, 6, 1, 0, 5]

given that 0 is index 4, we swap x[4] <=> x[7] or 
x[i] <=> x[i+N] where i is the index of 0