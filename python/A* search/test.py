from main import *

assert 548126730 == createStateNumber([5, 4, 8, 1, 2, 6, 7, 3, 0])

x = [1, 2, 6, 8, 5, 3, 7, 4, 0]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
assert evaluateToGoal(x,goal) == 6

queue = collections.deque()

