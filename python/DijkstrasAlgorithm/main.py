import time as time
import collections
import math

xi = [5, 4, 8, 1, 2, 6, 7, 3, 0] #initial state
xG = [1, 2, 3, 4, 5, 6, 7, 8, 0] #goal state
N = 3 #number of tiles on side
maxStates = 362880

# xi = [5, 1, 7, 3, 6, 0, 11, 2, 9, 4, 10, 8, 13, 14, 15, 12]
# xG = [7,11,13,5,4,10,2,6,0,1,5,8,13,9,14,12] #goal state
# # xG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #goal state
# N = 4 #number of tiles on side
# maxStates = 20922789888000

queue = collections.deque() #the queue
reachedStates = {} #dictionary to hold the stateNbr as key referencing the intersection (which holds the stateList, dist, etc about that state)

goalReached = False #if we have reached the goal or not
nbrReached = 0

class intersection: #or node
    def __init__(self, stateList, dist):
        self.stateList = stateList # [5, 4, 8, 1, 2, 6, 7, 3, 0]
        self.dist = dist # the current shortest distance from the start
        self.path = []
        self.stateNbr = createStateNumber(self.stateList)
        self.nextStates = returnxprime(self.stateList)
        self.nextStatesNbrs = list(map(createStateNumber, self.nextStates)) #Stores the state number (ie 548126730 for state, [5, 4, 8, 1, 2, 6, 7, 3, 0])
        self.heuristic = self.dist

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
    items = [queue.pop() for x in range(len(queue))] #gives a list of keys
    intersections = []
    for key in items:
        intersections.append(reachedStates[key])
    intersections.sort(key = lambda x: x.heuristic)
    stateNbrs = []
    for intersectionSorted in intersections:
        stateNbrs.append(intersectionSorted.stateNbr)
    queue.extend(stateNbrs)
    
def main():
    global nbrReached
    global goalReached
    startTime = time.time()

    head = intersection(xi, 0)
    goalNbr = createStateNumber(xG)
    reachedStates[createStateNumber(head.stateList)] = head
    queue.append(head.stateNbr)
    nbrReached+=1

    while queue and not goalReached:
        sortQueue(queue)
            
        currentStateNbr = queue.popleft()
        currentIntersection = reachedStates[currentStateNbr]
        
        if goalNbr == currentStateNbr:
            goalReached = True
            nextIntersection = intersection(xG, newDist)
            nextIntersection.path = currentIntersection.path + [currentStateNbr]
            queue.append(nextIntersection.stateNbr)
            reachedStates[currentStateNbr] = nextIntersection
            break
        
        for inx, stateNbr in enumerate(currentIntersection.nextStatesNbrs):
            newDist = currentIntersection.dist + 1 #each move is the same so just add 1

            #check if already reached
            if stateNbr in reachedStates:
                pass
                oldDist = reachedStates[stateNbr].dist
                if newDist < oldDist:
                    reachedStates[stateNbr].dist = newDist #update the next state distance
                    reachedStates[stateNbr].path = currentIntersection.path + [stateNbr]
                    
            else:
                nbrReached+=1
                if nbrReached%1000 == 0:
                    print(stateNbr)
                    print("Reached:",nbrReached, "\tPercentage:", round((nbrReached/maxStates)*100), "%")
                nextIntersection = intersection(currentIntersection.nextStates[inx], newDist)
                nextIntersection.path = currentIntersection.path + [stateNbr]
                queue.append(nextIntersection.stateNbr)
                reachedStates[stateNbr] = nextIntersection
                
    endTime = time.time()
    totalTime = endTime - startTime 
    print("Finished in " + str(round(totalTime/60)) + " min, " + str(round(totalTime%60)) + " secs, " + str(round(((totalTime%60)*1000)%1000)) + " ms\n")
    print("Reached:",nbrReached,"states")
    print("Shortest path to goal:", reachedStates[goalNbr].dist)

    for path in reachedStates[goalNbr].path:
        if path < 100000000:
            print("0" + str(path),"->")
        else:
            print(path,"->")


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

def returnxprime(state): #state is a list [5, 4, 8, 1, 2, 6, 7, 3, 0]
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