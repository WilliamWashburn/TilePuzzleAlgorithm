def printStates(listOfStateObjs):
    for stateObj in listOfStateObjs:
        print(stateObj.state)


# def generalForwardSearch(xi, XG, N):
#     Q = Queue(xi)
#     G = GoalState(XG)
#     D = DeadStateTracker()
#     stateTracker = ReachedStateTracker()
#     while Q.queue:
#         state = Q.getFirst()
#         if G.checkIfGoalReached(state):
#             print("goal reached!")
#             break
#         for primeX in state.returnxprime():
#             if not stateTracker.checkIfReached(primeX):
#                 # print(primeX.state)
#                 stateTracker.reachedStates.append(primeX)
#                 Q.queue.append(primeX)
#                 stateTracker.nbrReached += 1
#                 if (stateTracker.nbrReached % 1000 == 0):
#                     print(stateTracker.nbrReached, (stateTracker.nbrReached/362880)*100,"%" )
#             else:
#                 pass
#                 # if(D.checkIfShouldBeDead(primeX,stateTracker.reachedStates,N)):
#                 #     Q.remove(primeX)
#                 #     D.appendToDead(primeX)
#     printStates(stateTracker.reachedStates)
#     print("Reached: ",len(stateTracker.reachedStates)," or ",stateTracker.nbrReached, " states")
def createStateNumber(state):
        stateStr = ""
        for i in state:
            stateStr += str(i)
        return int(stateStr)

def step(Q,G,S,N):
    if not Q.queue:
        print("Q empty!")
        return
    state = Q.getFirst()
    if G.checkIfGoalReached(state):
        print("goal reached! -->", str(state.state))
        G.goalReached(True) #set goal reached flag
        return
    for primeX in state.returnxprime():
        if S.checkIfReached(primeX):
            # print("Rejecting",str(primeX.state))
            pass
        else:
            S.addReachedState(primeX)
            Q.queue.append(primeX)
            S.nbrReached += 1
            if (S.nbrReached % 1000 == 0):
                print(S.nbrReached, (S.nbrReached/362880)*100,"%" )

def stepNumberOfTimes(nbrOfTimes,Q,G,D,S,N):
    print("Step 0")
    printStates(Q.queue)
    print()

    for i in range(1,nbrOfTimes):
        print("\033[4mStep",i,"\033[0m")
        step(Q,G,D,S,N)
        print("Q")
        printStates(Q.queue)
        print()

