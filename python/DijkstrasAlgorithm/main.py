import time as time
import collections
import math

xi = [5, 4, 8, 1, 2, 6, 7, 3, 0] #initial state
xG = [1, 2, 3, 4, 5, 6, 7, 8, 0] #goal state
N = 3 #number of tiles on side

# # xi = [5, 1, 7, 3, 6, 0, 11, 2, 9, 4, 10, 8, 13, 14, 15, 12]
# xi = [1, 13, 5, 10, 2, 7, 15, 4, 9, 8, 10, 12, 3, 11, 14, 0]
# # xG = [7, 11, 13, 5, 4, 10, 2, 6, 0,1,5,8,13,9,14,12] #goal state
# xG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #goal state
# N = 4 #number of tiles on side

previousNbr = {}
distToState = {}
distToGoal = {}
heuristic = {}
stateLists = {}
prevMove = {}

queue = collections.deque() #intersection class
reachedStates = set() #stateNbrs

def main():
    nbrReached = 0
    goalReached = False

    startTime = time.time()

    goalNbr = createStateNumber(xG)
    stateNbr = createStateNumber(xi)
    
    reachedStates.add(stateNbr)
    queue.append(stateNbr)
    
    previousNbr[stateNbr] = None
    distToState[stateNbr] = 0
    distToGoal[stateNbr] = evaluateToGoal(xi, xG)
    heuristic[stateNbr] = calcHeuristic(stateNbr)
    prevMove[stateNbr] = None
    stateLists[stateNbr] = xi

    nbrReached+=1

    while queue and not goalReached:
        currentStateNbr, currentInx = getStateNbrWithMinHeurisitic()
        del queue[currentInx]
        
        if goalNbr == currentStateNbr:
            print("Goal Reached!")
            goalReached = True
            break
        
        nextStates, moveList = returnxprime(stateLists[currentStateNbr])
        nextStateNbrs = list(map(createStateNumber, nextStates)) 
        for inx, nextStateNbr in enumerate(nextStateNbrs):
            newDist = distToState[currentStateNbr] + 1 #each move is the same so just add 1

            #check if already reached
            if nextStateNbr in reachedStates:
                oldDist = distToState[nextStateNbr]
                if newDist < oldDist:
                    previousNbr[nextStateNbr] = currentStateNbr
                    distToState[nextStateNbr] = newDist
                    heuristic[nextStateNbr] = calcHeuristic(nextStateNbr)
                    prevMove[nextStateNbr] = moveList[inx]
            else:
                nbrReached+=1
                if nbrReached%1000 == 0:
                    printQueue()
                    print("Reached:",nbrReached,"\n")
                previousNbr[nextStateNbr] = currentStateNbr
                distToState[nextStateNbr] = newDist
                distToGoal[nextStateNbr] = evaluateToGoal(nextStates[inx], xG)
                heuristic[nextStateNbr] = calcHeuristic(nextStateNbr)
                stateLists[nextStateNbr] = nextStates[inx]
                prevMove[nextStateNbr] = moveList[inx]
                
                queue.append(nextStateNbr)
                reachedStates.add(nextStateNbr)

                
    endTime = time.time()
    totalTime = endTime - startTime 

    if goalReached:
        printPath()
    print("Finished in " + str(round(totalTime/60)) + " min, " + str(round(totalTime%60)) + " secs, " + str(round(((totalTime%60)*1000)%1000)) + " ms\n")
    print("Reached:",nbrReached,"states")

def getStateNbrWithMinHeurisitic():
    currentStateNbr = queue[0]
    currentInx = 0
    for inx, comparedStateNbr in enumerate(queue):
        if heuristic[comparedStateNbr] < heuristic[currentStateNbr]:
            currentStateNbr = comparedStateNbr
            currentInx = inx
    return currentStateNbr, currentInx

def calcHeuristic(stateNbr):
    heuristic = distToGoal[stateNbr] + distToState[stateNbr]
    # heuristic = distToGoal[stateNbr]
    # heuristic = distToState[stateNbr]
    return heuristic
        
def evaluateToGoal(state, goal):
    sum = 0
    for inx, pos in enumerate(state):
        desiredInx = goal.index(pos)
        rowDist = abs(inx % N - desiredInx % N)
        columnDist = abs(math.floor(inx/N) - math.floor(desiredInx/N))
        # print("For: ", pos, "\n", rowDist,",",columnDist)
        sum += (columnDist+rowDist)
    return sum

def printQueue():
    queueLength = len(queue)
    if queueLength > 10:
        for beginning in range(0,5):
            state = queue[beginning]
            print(stateLists[state], heuristic[state])
        print("...")
        for end in range(queueLength-1,queueLength-6,-1):
            state = queue[end]
            print(stateLists[state], heuristic[state])
    else:
        for state in queue:
            print(stateLists[state], heuristic[state])

def printPath():
    count = 0
    prevNbr = createStateNumber(xG)
    while prevNbr != None:
        print(prevNbr, "->", prevMove[prevNbr])
        prevNbr = previousNbr[prevNbr]
        count += 1
    print("Path length", count)

def createStateNumber(state):
    stateStr = ""
    for i in state:
        stateStr += str(i)
    return int(stateStr)

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
    moveList = []
    zeroPosition = state.index(0)
    #check corners
    if zeroPosition == 0:
        #top left corner, only right and bottom
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
        moveList = ["R","B"]
    elif zeroPosition == N - 1:
        #top right corner, only left and bottom
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
        moveList = ["L","B"]
    elif zeroPosition == (N*N)-1:
        #bottom right corner, only left and top
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
        moveList = ["T","L"]
    elif zeroPosition == (N*N)-N:
        #bottom left corner, only top and right
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        moveList = ["T","R"]
    
    #check edges
    elif zeroPosition < N - 1:
        #zero along top, only left,right,bottom
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(bottomMovement(state, zeroPosition))
        moveList = ["L","R","B"]
    elif (N*N)-N < zeroPosition < (N*N)-1:
        #zero along bottom, only left,right,top
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
        moveList = ["L","R","T"]
    elif zeroPosition % N == 0:
        #zero along left side, only right,top, bottom
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
        moveList = ["B","R","T"]
    elif zeroPosition % N == 2:
        #zero along right side, only left,top, bottom
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
        moveList = ["B","L","T"]
    else:
        xprimeList.append(bottomMovement(state, zeroPosition))
        xprimeList.append(leftMovement(state, zeroPosition))
        xprimeList.append(topMovement(state, zeroPosition))
        xprimeList.append(rightMovement(state, zeroPosition))
        moveList = ["B","L","T","R"]
    
    return xprimeList, moveList
    # return xprimeList

if __name__ == "__main__":
    main()