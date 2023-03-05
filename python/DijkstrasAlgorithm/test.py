import time as time
from main import evaluateToGoal
import numpy as np

# goal = [0,1,2,3,4,5,6,7,8]
# currentState = [1,0,2,3,8,5,6,7,4]
goal = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
currentState = [1,0,2,3,8,5,6,7,4,9,10,11,12,13,14,15]

startTime = time.time()
dist = evaluateToGoal(goal,currentState)
endTime = time.time()
totalTime = endTime - startTime

print(totalTime,dist)

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

startTime = time.time()
dist = manhattan(goal,currentState)
endTime = time.time()
totalTime = endTime - startTime

print(totalTime,dist)

def withNumpy(a,b):
    dist = np.sum(np.abs(a - b))
    return dist

goalNP = np.array(goal)
currentStateNP = np.array(currentState)
startTime = time.time()
dist = withNumpy(goalNP,currentStateNP)
endTime = time.time()
totalTime = endTime - startTime

print(totalTime,dist)










