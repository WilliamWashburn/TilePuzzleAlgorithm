#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cstdlib> 
#include <math.h>
#include <chrono>
#include <sstream>
using namespace std;
using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;

const int maxNbrOfStates = 500000;
const int N = 3; //number of tiles on side
const int nbrOfTiles = 9; //not sure how to make this a const of pow(nbrOfTiles,2)
int xi[] = {5, 4, 8, 1, 2, 6, 7, 3, 0}; //initial state REACHABLE
int xG[] = {0, 2, 3, 4, 5, 6, 7, 8, 0}; //goal state REACHABLE
// int xG[] = {1, 2, 3, 4, 5, 6, 7, 8, 0}; //goal state REACHABLE
int reachedStates[maxNbrOfStates][nbrOfTiles]; //array of state arrays
int reachedStatesLength = 0; //how many states we have reached. Index of the last reached state in the reachedStates array
int reachedStatesNumbers[maxNbrOfStates]; //we will store the states here as numbers ie. [5, 4, 8, 1, 0, 6, 7, 2, 3] -> 548106723 to make it faster to check if we have reached the state
int* queue[maxNbrOfStates]; //the queue. Holds pointers to states stored in reachedStates[]
int frontOfQueue = 0; //keep track of the front of the queue
int endOfQueue = 0; //keeps track of the end of the queue

bool goalReached = false; //if we have reached the goal or not

//turns a state [5, 4, 8, 1, 0, 6, 7, 2, 3] into a number 548106723 to store in reachedStatesNumbers[]. This makes it faster to check if a state has been reached becase we dont have to compare each element in the list, just a single number representing that list
int createStateNumber(int state[]){
    char stateStr[12];
    strcpy(stateStr,to_string(state[0]).c_str());;
    for (int i = 1; i < N*N-1; i++){
        strcat(stateStr,to_string(state[i]).c_str());;
    }
    return atoi(stateStr);
}

//for printing a state, just pass the pointer to the beginning of the array
void printState(int* state) {
    std::cout << "[";
    for (int i = 0; i < nbrOfTiles; i++){
        std::cout << state[i];
        if (i != nbrOfTiles - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "]";
    std::cout << endl;
}

//REACHED STATES
//add state to reachedStates[] and reachedStatesNumbers[]
void addReachedState(int* state) {
    for(int i = 0; i < nbrOfTiles; i++){
        reachedStates[reachedStatesLength][i] = state[i]; //copy the state
    }
    reachedStatesNumbers[reachedStatesLength] = createStateNumber(state);
    reachedStatesLength++;
}

void printReachedStates() {
    std::cout << "reachedStatesLength: " << reachedStatesLength << std::endl;
    std::cout << "Reached States: " << std::endl;
    for (int i = 0; i < reachedStatesLength; i++){
        std::cout << "[";
        for (int j = 0; j < nbrOfTiles; j++){
            std::cout << reachedStates[i][j];
            if (j != nbrOfTiles - 1) {
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }
}

bool checkifReached(int* state){
    int stateNbr = createStateNumber(state);
    for (int i = 0; i < reachedStatesLength; i++){
        if(reachedStatesNumbers[i] == stateNbr) {
            return true;
        }
    }
    return false;
}

//QUEUED STATES
// add state to queue[]. queue[] just stores pointers to arrays in reachedStates[][]
void addToQueue(int* reachedState) {
    queue[endOfQueue] = reachedState;
    endOfQueue++;
}

//return the first pointer in the queue, moves the front of the queue forward
int* getFirstFromQueue() {
    if (endOfQueue == 0) {
        std::cout << "queue length equal to 0! Can't shift" << std::endl;
        return nullptr;
    }
    if (endOfQueue > maxNbrOfStates) {
        std::cout << "queue overflow! Can't shift" << std::endl;
        return nullptr;
    }
    int* ptrToFirst = queue[frontOfQueue];
    frontOfQueue++;
    return ptrToFirst;
}

void printQueue() {
    std::cout << "QueueLength: " << endOfQueue - frontOfQueue << std::endl;
    std::cout << "Queue: " << std::endl;
    for (int i = frontOfQueue; i < endOfQueue; i++){
        int* ptrToState = queue[i];
        printState(ptrToState);
    }
    std::cout << endl;
}

bool checkIfGoalReached(int* statePtr) {
    // I tried to use the stateNbr like with the reached states but its not much faster than to just check each element. It could be helpful if there were many goal states
    int stateNbr = createStateNumber(statePtr);
    static int xGNbr = createStateNumber(xG);
    if (stateNbr != xGNbr) {
        return false;
    }
    for (int i = 0; i < nbrOfTiles; i++) {
        if (statePtr[i] != xG[i]) {
            return false;
        }
    }
    printState(statePtr);
    return true;
}

int findZeroPosition(int* state) {
    for (int i = 0; i < nbrOfTiles; i++){
        if (state[i] == 0) {
            return i;
        }
    }
    return -1;
}

void copyState(int* state,int* newState){
    for (int i = 0; i < nbrOfTiles; i++){
        newState[i] = state[i];
    }
}
void rightMovement(int* state, int* newState){
    // x[i] <=> x[i+1]
    int zeroPosition = findZeroPosition(state);
    copyState(state,newState);
    newState[zeroPosition] = state[zeroPosition + 1];
    newState[zeroPosition + 1] = state[zeroPosition];
}

void leftMovement(int* state, int* newState){
    // x[i] <=> x[i-1]
    int zeroPosition = findZeroPosition(state);
    copyState(state,newState);
    newState[zeroPosition] = state[zeroPosition - 1];
    newState[zeroPosition - 1] = state[zeroPosition];
}
void topMovement(int* state, int* newState){
    //x[i] <=> x[i-N]
    int zeroPosition = findZeroPosition(state);
    copyState(state,newState);
    newState[zeroPosition] = state[zeroPosition - N];
    newState[zeroPosition - N] = state[zeroPosition];
}

void bottomMovement(int* state, int* newState){
    //x[i] <=> x[i-N]
    int zeroPosition = findZeroPosition(state);
    copyState(state,newState);
    newState[zeroPosition] = state[zeroPosition + N];
    newState[zeroPosition + N] = state[zeroPosition];
}

int returnxprime(int* state, int* primeStates){
    int moveNbr = 0;
    int zeroPosition = findZeroPosition(state);
    //check corners
    if (zeroPosition == 0) {
        //top left corner, only right and bottom
        rightMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        bottomMovement(state,primeStates); moveNbr++;
    }
    else if(zeroPosition == N - 1){
        //top right corner, only left and bottom
        leftMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        bottomMovement(state,primeStates); moveNbr++;
    }
    else if(zeroPosition == N*N-1){
        //bottom right corner, only left and top
        topMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        leftMovement(state,primeStates); moveNbr++;
    }
    else if(zeroPosition == N*N-N){
        //bottom left corner, only top and right
        topMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        rightMovement(state,primeStates); moveNbr++;
    }
    
    //check edges
    else if(zeroPosition < N){
        //zero along top, only left,right,bottom
        leftMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        rightMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        bottomMovement(state,primeStates); moveNbr++;
    }
    else if((N*N-N < zeroPosition) && (zeroPosition < N*N-1)){
        //zero along bottom, only left,right,top
        leftMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        rightMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        topMovement(state,primeStates); moveNbr++;
    }
    else if(zeroPosition % N == 0){
        //zero along left side, only right,top, bottom
        bottomMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        rightMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        topMovement(state,primeStates); moveNbr++;
    }
    else if(zeroPosition % N == 2){
        //zero along right side, only left,top, bottom
        bottomMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        leftMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        topMovement(state,primeStates); moveNbr++;
    }
    else{
        bottomMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        leftMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        topMovement(state,primeStates); moveNbr++;
        primeStates += nbrOfTiles;
        rightMovement(state,primeStates); moveNbr++;
    }
    
    return moveNbr;
}

void step(){
    if((endOfQueue - frontOfQueue) == 0) {
        std::cout << "The queue is empty. Can't step" << std::endl;
        return;
    }
    
    int* firstState = getFirstFromQueue();
    // print("firstState:",firstState)
    if (checkIfGoalReached(firstState)){
        std::cout << "Goal Reached!" << std::endl;
        goalReached = true;
        return;
    }

    int xprimes[4][9];
    int nbrOfNewStates = returnxprime(firstState, &xprimes[0][0]);
    for(int i = 0; i < nbrOfNewStates; i++){
        // print("xprime:",xprime)
        if (!checkifReached(&xprimes[i][0])){
            addReachedState(&xprimes[i][0]);
            addToQueue(&reachedStates[endOfQueue-1][0]);
            if (reachedStatesLength%1000 == 0){
                std::cout << "Reached: " << reachedStatesLength << std::endl;
            }
        }
    }
}

int main(){
    std::cout << "Beginning!" << std::endl;
    addReachedState(xi);
    addToQueue(&reachedStates[0][0]);
    std::cout << createStateNumber(&reachedStates[0][0]) << std::endl;

    auto t1 = high_resolution_clock::now();
    while ((endOfQueue - frontOfQueue) > 0 && !goalReached){
        // std::cout << "Press Enter to continue" << std::endl;
        // getchar();
        step();
        // printQueue();
    }
    if ((endOfQueue - frontOfQueue) == 0) {
        std::cout << "Queue is empty" << std::endl;
    }

    auto t2 = high_resolution_clock::now();
    auto ms_int = duration_cast<milliseconds>(t2 - t1);

    std::cout << "Total time: " << round((ms_int.count()/1000)/60) << " min, " <<  round(((ms_int.count()/1000))%60)<< " secs, " << round(ms_int.count()%1000) << " ms" << std::endl;
    std::cout << "Reached: ";
    std::cout << reachedStatesLength;
    std::cout << " states"; std::cout<<"\n";
}