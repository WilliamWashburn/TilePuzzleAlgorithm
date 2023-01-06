def DeadStateTrackerTest():
    from classes import stateObject
    from classes import DeadStateTracker

    xi = stateObject([3, 4, 7, 2, 0, 6, 1, 8, 5]) #initial state
    D = DeadStateTracker()
    N = 3
    D.checkIfShouldBeDead(xi,xi.returnxprime(N),3)
