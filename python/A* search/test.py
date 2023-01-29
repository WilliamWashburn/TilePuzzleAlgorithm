from main import *

# assert 548126730 == createStateNumber([5, 4, 8, 1, 2, 6, 7, 3, 0])

# x = [1, 2, 6, 8, 5, 3, 7, 4, 0]
# goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# assert evaluateToGoal(x,goal) == 6

# def printQueue():
#     for state in queue:
#         print(reachedStates[state].stateList, reachedStates[state].heuristic)
# queue = []
# reachedStates = {}

# aintersection = intersection([1, 2, 3, 6, 5, 4, 7, 8, 0],0)
# reachedStates[aintersection.stateNbr] = aintersection
# queue.append(aintersection.stateNbr)

# aintersection = intersection([1, 2, 3, 4, 5, 6, 7, 8, 0],0)
# reachedStates[aintersection.stateNbr] = aintersection
# queue.append(aintersection.stateNbr)

# aintersection = intersection([1, 2, 6, 8, 5, 3, 7, 4, 0],0)
# print(aintersection.stateNbr)
# reachedStates[aintersection.stateNbr] = aintersection
# queue.append(aintersection.stateNbr)

# printQueue()
# print("Sorting")
# sortQueue(queue,reachedStates)
# printQueue()

print(evaluateToGoal([1, 13, 5, 10, 9, 2, 7, 4, 3, 0, 11, 8, 14, 6, 15, 12],[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]))