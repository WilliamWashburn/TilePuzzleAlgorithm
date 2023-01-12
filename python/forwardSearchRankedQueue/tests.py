def main():
    DeadStateTrackerTest()
    GoalTest()
    xprimetest()
    checkIfReachedTest()
    CreateStateNumberTest()
    sortQueueTest()

def xprimetest():
    from classes import stateObject
    N = 3
    x = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N)
    xprimes = x.returnxprime()
    assert (xprimes[0].state == [3, 4, 7, 2, 8, 6, 1, 0, 5])
    assert (xprimes[1].state == [3, 4, 7, 0, 2, 6, 1, 8, 5])
    assert (xprimes[2].state == [3, 0, 7, 2, 4, 6, 1, 8, 5])
    assert (xprimes[3].state == [3, 4, 7, 2, 6, 0, 1, 8, 5])

def sortQueueTest():
    from classes import stateObject
    from classes import Queue
    N = 3
    xi = stateObject([7, 4, 5, 3, 8, 0, 1, 6, 2],N)
    Q = Queue(xi)
    printStates([Q.getFirst()])

def checkIfReachedTest():
    from classes import ReachedStateTracker
    from classes import stateObject
    N = 3
    x = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N)
    S = ReachedStateTracker()
    assert(S.checkIfReached(x) == False)
    S.addReachedState(x)
    assert(S.checkIfReached(x) == True)

def CreateStateNumberTest():
    from classes import ReachedStateTracker
    from classes import stateObject
    N = 3
    x = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N)
    S = ReachedStateTracker()
    stateNbr = createStateNumber(x.state)
    assert(stateNbr == 347206185)

def DeadStateTrackerTest():
    from classes import stateObject
    from classes import DeadStateTracker
    N = 3

    xi = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N) #initial state
    D = DeadStateTracker()
    N = 3
    assert (True == D.checkIfShouldBeDead(xi,xi.returnxprime(),N))
    assert (False == D.checkIfShouldBeDead(xi,[stateObject(xi.rightMovement(),N)],N))

def GoalTest():
    from classes import stateObject
    from classes import GoalState
    N = 3
    xG = stateObject([1,2,3,4,5,6,7,8,0],N)
    G = GoalState([xG])
    assert (True == G.checkIfGoalReached(xG))
    x = stateObject([0,1,2,3,4,5,6,7,8],N)
    assert (False == G.checkIfGoalReached(x))

    assert (False == G.ifReached)
    G.goalReached(True)
    assert (True == G.ifReached)


if __name__ == "__main__":
    from functions import createStateNumber
    from functions import printStates
    main()