import time as time
import collections

xi = [5, 4, 8, 1, 2, 6, 7, 3, 0] #initial state
xG = [1, 2, 3, 4, 5, 6, 7, 8, 0] #goal state
N = 3 #number of tiles on side
maxStates = 362880

# xi = [5, 1, 7, 3, 6, 0, 11, 2, 9, 4, 10, 8, 13, 14, 15, 12]
# xG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #goal state
# N = 4 #number of tiles on side
# maxStates = 20922789888000

queue = collections.deque() #the queue
reachedStates = {}
goalReached = False #if we have reached the goal or not
nbrReached = 0

def main():
    global nbrReached
    startTime = time.time()
    reachedStates[createStateNumber(xi)] = None
    queue.append(xi)
    nbrReached += 1
    while queue:
        step()
        if goalReached:
            break
    endTime = time.time()
    totalTime = endTime - startTime 
    print("Finished in " + str(round(totalTime/60)) + " min, " + str(round(totalTime%60)) + " secs, " + str(round(((totalTime%60)*1000)%1000)) + " ms\n")
    print("Reached:",nbrReached,"states")

    pathLength = 0
    prevState = reachedStates[createStateNumber(xG)]
    while prevState is not None:
        if prevState < 100000000:
            print("0"+str(prevState),"->")
        else:
            print(prevState,"->")
        pathLength += 1
        prevState = reachedStates[prevState]
    print("pathLength:",pathLength)

def createStateNumber(state):
    stateStr = ""
    for i in state:
        stateStr += str(i)
    return int(stateStr)

def step():
    global nbrReached
    global goalReached
    if not queue:
        print("The queue is empty")
        return
    
    currentState = queue.popleft()
    if currentState == xG:
        print("Goal Reached!")
        goalReached = True
        return
    for xprime in returnxprime(currentState):
        if checkifReached(xprime):
            pass
        else:
            reachedStates[createStateNumber(xprime)] = createStateNumber(currentState)
            queue.append(xprime)
            nbrReached += 1
            # if nbrReached%100000 == 0:
            #     print("Reached:",nbrReached, "\tPercentage:", round((nbrReached/maxStates)*100), "%")

def checkifReached(state):
    stateNbr = createStateNumber(state)
    if stateNbr in reachedStates:
        return True
    return False


def rightMovement(state, zeroPosition):
    # x[i] <=> x[i+1]
    newState = state.copy()
    newState[zeroPosition] = state[zeroPosition + 1]
    newState[zeroPosition + 1] = state[zeroPosition]
    return newState

def leftMovement(state, zeroPosition):
    # x[i] <=> x[i-1]
    newState = state.copy()
    newState[zeroPosition] = state[zeroPosition - 1]
    newState[zeroPosition - 1] = state[zeroPosition]
    return newState

def topMovement(state, zeroPosition):
    #x[i] <=> x[i-N]
    newState = state.copy()
    newState[zeroPosition] = state[zeroPosition - N]
    newState[zeroPosition - N] = state[zeroPosition]
    return newState

def bottomMovement(state, zeroPosition):
    #x[i] <=> x[i-N]
    newState = state.copy()
    newState[zeroPosition] = state[zeroPosition + N]
    newState[zeroPosition + N] = state[zeroPosition]
    return newState

def returnxprime(state):
    xprimeList = [] # a list of all the new possible states
    zeroPosition = state.index(0)
    #check corners
    if zeroPosition == 0:
        #top left corner, only right and bottom
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
    elif zeroPosition == N - 1:
        #top right corner, only left and bottom
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
    elif zeroPosition == (N*N)-1:
        #bottom right corner, only left and top
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
    elif zeroPosition == (N*N)-N:
        #bottom left corner, only top and right
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
    
    #check edges
    elif zeroPosition < N - 1:
        #zero along top, only left,right,bottom
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
    elif (N*N)-N < zeroPosition < (N*N)-1:
        #zero along bottom, only left,right,top
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
    elif zeroPosition % N == 0:
        #zero along left side, only right,top, bottom
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
    elif zeroPosition % N == 2:
        #zero along right side, only left,top, bottom
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
    else:
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
    
    return xprimeList

if __name__ == "__main__":
    main()