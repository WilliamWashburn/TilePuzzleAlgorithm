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

This is explained more throughly here: [appendix](appendix/movementDefinitions.md)

## Queue
The queue holds the states that have been reached but have adjacents states that still need to be explored. The different search algorithms use different strategies for chosing states from the queue or even sorting the queue. 

## Feasibility
For now, I just want to see how long it takes to go from the starting state to the goal state. We will search through the state space without keeping track of which action was applied. Additionally, these algorithms don't necessarily give us the shortest path between two states, just a feasible path.

## Benchmarking
To benchmark each search algorithm, I will search through the entire solution space from an arbitary initial state, [5, 4, 8, 1, 2, 6, 7, 3, 0]. I will also give a time from this initial state to the goal state.

## FIFO (First In, Fist Out)
The queue is sorted by "First in, First out". When we take a state off of the queue, it will have been in the queue the longest. When we add to the queue, it goes in the back. As we take states out of the queue, the elements slide forward in priority.

Trial: [python/forwardSearchFIFO/main.py](python/forwardSearchFIFO/main.py)

**Whole solution space:** 9 min, 19 secs with 181440 states reached
**To the goal:** 2 min, 58 secs with 103359 states reached
Not very fast!

I want to see if I am slowing python down by having all the functions being broken out in classes. To test this, I'm simiplying everything to as "barebones" python as I know how.

Trial: [python/forwardSearchFIFO/simplifiedVersion/main.py](python/forwardSearchFIFO/simplifiedVersion/main.py)

**Whole solution space:** 9 min, 19 secs reaching 181440 states
**To the goal:** 2 min, 55 secs reaching 103359 states

This didn't improve performance at all. I know that this search method is not very fast, but how much faster would C++ be?

I rewrote the program in C++ just to see how much faster it could be. Here are the results:
Trial: [c++/FIFO.cpp](c++/FIFO.cpp)

**Whole solution space:** 1 min, 46 secs reaching 181440 states
**To the goal:** 20 secs reaching 103359 states

Thats definitely faster!

# Notes
You might have notices that the search algorithm only goes through 181440 states instead of the expected 9! or 362880 states. Thats because there are certain states (half of them) that cannot be reached from the other half of states. For example, if we have:
    [ 0 1 2
      3 4 5
      6 8 7 ]
There are no possible actions that can be applied to reached:
    [ 0 1 2
      3 4 5
      6 7 8 ]

## Dijkstra’s Algorithm
This search algorithm is good for finding the shortest paths. Its not really useful for our use case because the cost to apply any of the actions is the same. It can be helpful to find the shortest path where we are finding the shortest number of moves where each move costs the same.

We start at the beginning state. For that state, we look at all the next states. If we have not reached that state before, we mark that state as reached and assign an initial distance to that state and path to that state. We will add this new state to the queue to check adjacent states. If we have reached the state, we compare the distance to that state through the current path to the previous distance to that state. If we found a shorter path, we update the distance to that state and the associated path. Once we have checked all adjacent states of the beginning state, we get the next state from the queue based on FIFO.

Trial: [python/DijkstrasAlgorithm/main.py](python/DijkstrasAlgorithm/main.py)

**Whole solution space:** 5 secs reaching 181440 states
**To the goal:** 3 secs reaching 125614 states giving shortest path of 22 moves



