# Classes
class Queue:
    def __init__(self,xi):
        self.queue = [xi]

    def getFirst(self):
        toReturn = self.queue[0]
        self.queue.pop(0)
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

class GoalState:
    def __init__(self, goalstates):
        self.goalstates = goalstates

    def checkIfGoalReached(self,state):
        for goalState in self.goalstates:
            if goalState.state == state.state:
                return True
        return False

class ReachedStateTracker:
    def __init__(self):
        self.reachedStates = []
        self.nbrReached = 0

    def checkIfReached(self, state):
        for reachedState in self.reachedStates:
            if reachedState.state == state.state:
                return True
        return False

class DeadStateTracker:
    def __init__(self):
        self.deadStates = []
    
    #check if all its next states are already reached
    def checkIfShouldBeDead(self,stateObj,reachedStates,N):
        # print(stateObj.state)
        # printStates(reachedStates)
        nextStates = stateObj.returnxprime(N)
        # printStates(nextStates)
        #check reached states

        # for i in nextStates:
        #     print(i.state)
        
        count = 0
        for aNextState in nextStates: #for each next state, check if already in reached states
            oneInReached = False
            #check if in reached states
            for aReachedStates in reachedStates:
                # print(aReachedStates.state)
                if(aNextState.state == aReachedStates.state):
                    #the next state is already reached!
                    oneInReached = True
                    count = count + 1
                    # print(aNextState.state)
                    # print(aReachedStates.state)
            # print(oneInReached)
        if (count == len(nextStates)):
            # print("all reached")
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

    def returnxprime(self,N):
        xprimeList = []

        #check corners
        if self.zeroPosition == 0:
            #top left corner, only right and bottom
            xprimeList.append(stateObject(self.rightMovement()))
            xprimeList.append(stateObject(self.bottomMovement()))
        elif self.zeroPosition == self.N - 1:
            #top right corner, only left and bottom
            xprimeList.append(stateObject(self.leftMovement()))
            xprimeList.append(stateObject(self.bottomMovement()))
        elif self.zeroPosition == self.N*self.N-1:
            #bottom right corner, only left and top
            xprimeList.append(stateObject(self.topMovement()))
            xprimeList.append(stateObject(self.leftMovement()))
        elif self.zeroPosition == self.N*self.N-self.N:
            #bottom left corner, only top and right
            xprimeList.append(stateObject(self.topMovement()))
            xprimeList.append(stateObject(self.rightMovement()))
        
        #check edges
        elif self.zeroPosition < self.N:
            #zero along top, only left,right,bottom
            xprimeList.append(stateObject(self.leftMovement()))
            xprimeList.append(stateObject(self.rightMovement()))
            xprimeList.append(stateObject(self.bottomMovement()))
        elif self.N*self.N-self.N < self.zeroPosition < self.N*self.N-1:
            #zero along bottom, only left,right,top
            xprimeList.append(stateObject(self.leftMovement()))
            xprimeList.append(stateObject(self.rightMovement()))
            xprimeList.append(stateObject(self.topMovement()))
        elif self.zeroPosition % self.N == 0:
            #zero along left side, only right,top, bottom
            xprimeList.append(stateObject(self.bottomMovement()))
            xprimeList.append(stateObject(self.rightMovement()))
            xprimeList.append(stateObject(self.topMovement()))
        elif self.zeroPosition % self.N == 2:
            #zero along right side, only left,top, bottom
            xprimeList.append(stateObject(self.bottomMovement()))
            xprimeList.append(stateObject(self.leftMovement()))
            xprimeList.append(stateObject(self.topMovement()))
        else:
            xprimeList.append(stateObject(self.bottomMovement()))
            xprimeList.append(stateObject(self.leftMovement()))
            xprimeList.append(stateObject(self.topMovement()))
            xprimeList.append(stateObject(self.rightMovement()))
        
        return xprimeList