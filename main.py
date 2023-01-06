from classes import Queue
from classes import stateObject
from classes import ReachedStateTracker
from classes import GoalState
from classes import DeadStateTracker
from functions import step

def main():
    N = 3 #3 by 3 grid of tiles
    xi = stateObject([0, 4, 7, 2, 8, 6, 1, 5, 3],N) #first state
    XG = [stateObject([1, 2, 3, 4, 5, 6, 7, 8, 0],N)] # a list of possible states

    Q = Queue(xi) #add the first state object to the queue
    G = GoalState(XG)
    D = DeadStateTracker()
    S = ReachedStateTracker()
    
    Q.printStates() #print the first state

    step(Q,G,D,S,N)

if __name__ == "__main__":
    main()


            