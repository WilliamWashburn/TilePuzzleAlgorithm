def main():
    DeadStateTrackerTest()
    GoalTest()
    xprimetest()
    checkIfReachedTest()

def xprimetest():
    from classes import stateObject
    N = 3
    x = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N)
    xprimes = x.returnxprime(N)
    assert (xprimes[0].state == [3, 4, 7, 2, 8, 6, 1, 0, 5])
    assert (xprimes[1].state == [3, 4, 7, 0, 2, 6, 1, 8, 5])
    assert (xprimes[2].state == [3, 0, 7, 2, 4, 6, 1, 8, 5])
    assert (xprimes[3].state == [3, 4, 7, 2, 6, 0, 1, 8, 5])

def checkIfReachedTest():
    from classes import ReachedStateTracker
    from classes import stateObject
    N = 3
    x = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N)
    S = ReachedStateTracker()
    assert(S.checkIfReached(x) == False)
    S.addReachedState(x)
    assert(S.checkIfReached(x) == True)

def DeadStateTrackerTest():
    from classes import stateObject
    from classes import DeadStateTracker
    N = 3

    xi = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5],N) #initial state
    D = DeadStateTracker()
    N = 3
    assert (True == D.checkIfShouldBeDead(xi,xi.returnxprime(N),N))
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
    main()