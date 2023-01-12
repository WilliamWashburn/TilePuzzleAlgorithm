# Classes
class Queue:
    def __init__(self,xi):
        self.queue = [xi]

    def getFirst(self):
        toReturn = self.queue.pop(0) #16% gain by using pop()
        return toReturn

    def printStates(self):
        for i in self.queue:
            print(i.state)
    
    def remove(self,state):
        inx = 0
        for i in self.queue:
            if state.state == i.state:
                self.queue.pop(inx)
                return
            inx = inx + 1
    
    def sortQueue(self):
        self.queue.sort(key = getattr(self,'score'))

class GoalState:
    def __init__(self, goalstates):
        self.goalstates = goalstates
        self.ifReached = False #flag for if goal reached

    def checkIfGoalReached(self,state):
        for goalState in self.goalstates:
            if goalState.state == state.state:
                return True
        return False

    def goalReached(self,inputboolan):
        self.ifReached = inputboolan

from functions import createStateNumber

class ReachedStateTracker:
    def __init__(self):
        self.reachedStates = []
        self.nbrReached = 0
        self.reachedStatesList = []

    def checkIfReached(self, state):
        stateStr = createStateNumber(state.state)
        if stateStr in self.reachedStates:
            return True
        return False
    
    def addReachedState(self,state):
        stateStr = createStateNumber(state.state)
        self.reachedStates.append(stateStr)
        self.reachedStatesList.append(state.state)

class DeadStateTracker:
    def __init__(self):
        self.deadStates = []
    
    #check if all its next states are already reached
    def checkIfShouldBeDead(self,stateObj,reachedStates,N):
        nextStates = stateObj.returnxprime()
        count = 0
        for aNextState in nextStates: #for each next state, check if already in reached states
            oneInReached = False
            #check if in reached states
            for aReachedStates in reachedStates:
                if(aNextState.state == aReachedStates.state):
                    #the next state is already reached!
                    oneInReached = True
                    count = count + 1
        if (count == len(nextStates)):
            return True
        else:
            return False

    def appendToDead(self,stateObj):
        self.deadStates.append(stateObj.state)

class stateObject:
    def __init__(self,stateOrder,N):
        self.state = stateOrder
        self.zeroPosition = self.getZeroPosition()
        self.N = N
        self.score = 9999

    def createScore(self,xG):
        inx = 0
        score = 0
        for nbr in self.state:
            # score += abs(nbr - inx)
            inx += 1

            

    def getZeroPosition(self):
        return self.state.index(0)

    def setZeroPosition(self):
        self.zeroPosition = self.getZeroPosition()

    def rightMovement(self):
        # x[i] <=> x[i+1]
        newState = self.state.copy()
        newState[self.zeroPosition] = self.state[self.zeroPosition + 1]
        newState[self.zeroPosition + 1] = self.state[self.zeroPosition]
        return newState

    def leftMovement(self):
        # x[i] <=> x[i-1]
        newState = self.state.copy()
        newState[self.zeroPosition] = self.state[self.zeroPosition - 1]
        newState[self.zeroPosition - 1] = self.state[self.zeroPosition]
        return newState

    def topMovement(self):
        #x[i] <=> x[i-N]
        newState = self.state.copy()
        newState[self.zeroPosition] = self.state[self.zeroPosition - self.N]
        newState[self.zeroPosition - self.N] = self.state[self.zeroPosition]
        return newState

    def bottomMovement(self):
        #x[i] <=> x[i-N]
        newState = self.state.copy()
        newState[self.zeroPosition] = self.state[self.zeroPosition + self.N]
        newState[self.zeroPosition + self.N] = self.state[self.zeroPosition]
        return newState

    def returnxprime(self):
        xprimeList = []

        #check corners
        if self.zeroPosition == 0:
            #top left corner, only right and bottom
            xprimeList.append(stateObject(self.rightMovement(),self.N))
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
        elif self.zeroPosition == self.N - 1:
            #top right corner, only left and bottom
            xprimeList.append(stateObject(self.leftMovement(),self.N))
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
        elif self.zeroPosition == self.N*self.N-1:
            #bottom right corner, only left and top
            xprimeList.append(stateObject(self.topMovement(),self.N))
            xprimeList.append(stateObject(self.leftMovement(),self.N))
        elif self.zeroPosition == self.N*self.N-self.N:
            #bottom left corner, only top and right
            xprimeList.append(stateObject(self.topMovement(),self.N))
            xprimeList.append(stateObject(self.rightMovement(),self.N))
        
        #check edges
        elif self.zeroPosition < self.N:
            #zero along top, only left,right,bottom
            xprimeList.append(stateObject(self.leftMovement(),self.N))
            xprimeList.append(stateObject(self.rightMovement(),self.N))
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
        elif self.N*self.N-self.N < self.zeroPosition < self.N*self.N-1:
            #zero along bottom, only left,right,top
            xprimeList.append(stateObject(self.leftMovement(),self.N))
            xprimeList.append(stateObject(self.rightMovement(),self.N))
            xprimeList.append(stateObject(self.topMovement(),self.N))
        elif self.zeroPosition % self.N == 0:
            #zero along left side, only right,top, bottom
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
            xprimeList.append(stateObject(self.rightMovement(),self.N))
            xprimeList.append(stateObject(self.topMovement(),self.N))
        elif self.zeroPosition % self.N == 2:
            #zero along right side, only left,top, bottom
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
            xprimeList.append(stateObject(self.leftMovement(),self.N))
            xprimeList.append(stateObject(self.topMovement(),self.N))
        else:
            xprimeList.append(stateObject(self.bottomMovement(),self.N))
            xprimeList.append(stateObject(self.leftMovement(),self.N))
            xprimeList.append(stateObject(self.topMovement(),self.N))
            xprimeList.append(stateObject(self.rightMovement(),self.N))
        
        return xprimeList