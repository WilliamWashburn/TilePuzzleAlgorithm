from classes import Queue
from classes import stateObject
from classes import ReachedStateTracker
from classes import GoalState
from classes import DeadStateTracker
from functions import step
import time as time

debug = False

def main(debug = False):
    N = 3 #3 by 3 grid of tiles
    xi = stateObject([5, 4, 8, 1, 2, 6, 7, 3, 0],N) #first state
    # XG = [stateObject([1, 2, 3, 4, 5, 6, 7, 8, 0],N)] # a list of possible states
    XG = [stateObject([7, 4, 5, 3, 8, 0, 1, 6, 2],N)] # a list of possible states

    Q = Queue(xi) #add the first state object to the queue
    G = GoalState(XG)
    D = DeadStateTracker()
    S = ReachedStateTracker()

    S.addReachedState(xi)

    startTime = time.time()

    #start file
    if(debug):
        filename = "queue" + str(startTime) + ".txt"
        file = open("queue.txt", "w")
        file.write("Step 0\n")
        print("Step 0\n")
        file.write(str(xi.state) + "\n\n")
        print(str(xi.state) + "\n\n")

    count = 0
    while Q.queue and not G.ifReached:
    # for inx in range(1,8000):
        if debug:
            pass
            # input("Press Enter to continue...")
        step(Q,G,D,S,N)
        if debug:
            file.write("Step " + str(count) + "\n")
            print("Step " + str(count) + "\n")
            for i in Q.queue:
                file.write(str(i.state) + "\n")
                print(str(i.state) + "\n")
            file.write("\n")
            count+=1
    if debug:
        file.close()

    endTime = time.time()
    totalTime = endTime - startTime
    print("Finished in", round(totalTime/60), "min,", round(totalTime%60), "secs,", round(((totalTime%60)*1000)%1000), "ms")
    if(len(Q.queue) == 0):
        print("The queue has been emptied")

    filename = "reachedStates" + str(startTime) + ".txt"
    f = open(filename, "w")
    f.write("Initial state: " + str(xi.state) + "\n")
    f.write("Goal state: " + str(XG[0].state) + "\n")
    f.write(str(S.nbrReached) + " states were reached\n")
    f.write("Finished in " + str(round(totalTime/60)) + " min, " + str(round(totalTime%60)) + " secs, " + str(round(((totalTime%60)*1000)%1000)) + " ms\n")
    for State in S.reachedStates:
        f.write(str(State.state))
        f.write("\n")
    f.close()
    print("Created a file called",filename,"containing all the reached states")

if __name__ == "__main__":
    main(debug)


            