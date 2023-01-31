import time as time
import collections
import math

# xi = [5, 4, 8, 1, 2, 6, 7, 3, 0] #initial state
# xG = [1, 2, 3, 4, 5, 6, 7, 8, 0] #goal state
# N = 3 #number of tiles on side
# maxStates = 362880

xi = [5, 1, 7, 3, 6, 0, 11, 2, 9, 4, 10, 8, 13, 14, 15, 12]
# xG = [7, 11, 13, 5, 4, 10, 2, 6, 0,1,5,8,13,9,14,12] #goal state
xG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #goal state
N = 4 #number of tiles on side
maxStates = 20922789888000

queue = collections.deque() #intersection class
reachedStates = {} #stateNbrs referencing distances

goalReached = False
nbrReached = 0

class intersection: #or node
    def __init__(self, stateList, dist):
        self.stateList = stateList # [5, 4, 8, 1, 2, 6, 7, 3, 0]
        self.dist = dist # the current shortest distance from the start
        self.path = []
        self.moveList = []
        self.stateNbr = createStateNumber(self.stateList)
        self.nextStates, self.nextMoves = returnxprime(self.stateList)
        self.nextStatesNbrs = list(map(createStateNumber, self.nextStates)) #Stores the state number (ie 548126730 for state, [5, 4, 8, 1, 2, 6, 7, 3, 0])
        self.distToGoal = evaluateToGoal(self.stateList, xG)
        self.calcHeuristic()
    
    def calcHeuristic(self):
        self.heuristic = (self.distToGoal + self.dist)
        # self.heuristic = (self.distToGoal)
        # self.heuristic = (self.dist)
        
def evaluateToGoal(state, goal):
    sum = 0
    for inx, pos in enumerate(state):
        desiredInx = goal.index(pos)
        rowDist = abs(inx % N - desiredInx % N)
        columnDist = abs(math.floor(inx/N) - math.floor(desiredInx/N))
        # print("For: ", pos, "\n", rowDist,",",columnDist)
        sum += (columnDist+rowDist)
    return sum

def sortQueue(queue):
    items = [queue.pop() for x in range(len(queue))]
    items.sort(key = lambda x: x.heuristic)
    queue.extend(items)
    

def printQueue():
    queueLength = len(queue)
    if queueLength > 10:
        for beginning in range(0,5):
            state = queue[beginning]
            print(reachedStates[state].stateList, reachedStates[state].heuristic, reachedStates[state].dist, reachedStates[state].distToGoal)
        print("...")
        for end in range(queueLength-1,queueLength-6,-1):
            state = queue[end]
            print(reachedStates[state].stateList, reachedStates[state].heuristic, reachedStates[state].dist, reachedStates[state].distToGoal)
    else:
        for state in queue:
            print(reachedStates[state].stateList, reachedStates[state].heuristic, reachedStates[state].dist, reachedStates[state].distToGoal)
    
def main():
    global nbrReached
    global goalReached
    startTime = time.time()

    head = intersection(xi, 0)
    goalNbr = createStateNumber(xG)
    reachedStates[head.stateNbr] = head
    queue.append(head)
    nbrReached+=1

    while queue and not goalReached:
        sortQueue(queue)
            
        currentIntersection = queue.popleft()
        currentStateNbr = currentIntersection.stateNbr
        
        if goalNbr == currentStateNbr:
            print("Goal Reached!")
            goalReached = True
            break
        
        for inx, stateNbr in enumerate(currentIntersection.nextStatesNbrs):
            newDist = currentIntersection.dist + 1 #each move is the same so just add 1

            #check if already reached
            if stateNbr in reachedStates:
                oldDist = reachedStates[stateNbr].dist
                if newDist < oldDist:
                    newMoveList = currentIntersection.moveList + [currentIntersection.nextMoves[inx]]
                    reachedStates[stateNbr].moveList = newMoveList
                    reachedStates[stateNbr].dist = newDist
                    reachedStates[stateNbr].path = currentIntersection.path + [stateNbr]
                    
            else:
                nbrReached+=1
                if nbrReached%1000 == 0:
                    print(stateNbr)
                    print("Reached:",nbrReached, "\tPercentage:", round((nbrReached/maxStates)*100), "%")
                nextIntersection = intersection(currentIntersection.nextStates[inx], newDist)
                nextIntersection.path = currentIntersection.path + [stateNbr]
                nextIntersection.moveList = currentIntersection.moveList + [currentIntersection.nextMoves[inx]]
                queue.append(nextIntersection)
                reachedStates[stateNbr] = nextIntersection        
                
    endTime = time.time()
    totalTime = endTime - startTime 
    print("Finished in " + str(round(totalTime/60)) + " min, " + str(round(totalTime%60)) + " secs, " + str(round(((totalTime%60)*1000)%1000)) + " ms\n")
    print("Reached:",nbrReached,"states")
    print("Shortest path to goal:", reachedStates[goalNbr].dist)

    # print(len(currentIntersection.path))
    for inx,path in enumerate(currentIntersection.path):
        if path < 100000000:
            print("0" + str(path),"->",currentIntersection.moveList[inx])
        else:
            print(path,"->",currentIntersection.moveList[inx])
            # print(path,"->")
    
    # print(len(reachedStates[goalNbr].moveList))
    # for move in reachedStates[goalNbr].moveList:
    #     print(move)


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
    
    firstState = queue.pop(0)
    if firstState == xG:
        print("Goal Reached!")
        goalReached = True
        return
    for xprime in returnxprime(firstState):
        if checkifReached(xprime):
            pass
        else:
            reachedStates.append(createStateNumber(xprime))
            queue.append(xprime)
            nbrReached += 1
            if nbrReached%1000 == 0:
                print("Reached:",nbrReached)

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

if __name__ == "__main__":
    main()