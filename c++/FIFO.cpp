#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cstdlib> 
#include <math.h>
#include <chrono>
#include <sstream>
#include <map>
#include <string> //stoull
using namespace std;
using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::duration;
using std::chrono::milliseconds;

// const int maxNbrOfStates = 362880;
// const int N = 3; //number of tiles on side
// const int nbrOfTiles = 9; //not sure how to make this a const of pow(nbrOfTiles,2)
// int xi[] = {5, 4, 8, 1, 2, 6, 7, 3, 0};
// int xG[] = {1, 2, 3, 4, 5, 6, 7, 8, 0};

const long maxNbrOfStates = 362880;
const int N = 4; //number of tiles on side
const int nbrOfTiles = 16; //not sure how to make this a const of pow(nbrOfTiles,2)
int xi[] = {1, 6, 2, 4, 5, 11, 10, 7, 13, 0, 3, 9, 14, 15, 12, 8}; //easy
// int xG[] = {6, 2, 3, 4, 1, 10, 0, 7, 13, 12, 11, 9, 5, 14, 15, 8};
int xG[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0};

//reached states
int nbrOfReachedStates = 0;
std::map<string,bool> reachedStatesStrings; //we will store the states here as numbers ie. [5, 4, 8, 1, 0, 6, 7, 2, 3] -> 548106723 to make it faster to check if we have reached the state

//queue
// const int queueSize = 362880;
const int queueSize = 24000;
int queue[queueSize][nbrOfTiles]; //the queue. Holds pointers to states stored in reachedStates[]
int frontOfQueue = 0; //keep track of the front of the queue
int endOfQueue = 0; //keeps track of the end of the queue
int maxSizeOfQueue = 0;

bool goalReached = false; //if we have reached the goal or not

//turns a state [5, 4, 8, 1, 0, 6, 7, 2, 3] into a number 548106723 to store in reachedStatesNumbers[]. This makes it faster to check if a state has been reached becase we dont have to compare each element in the list, just a single number representing that list
// int createStateNumber(int* state){
//     char stateStr[30];
//     strcpy(stateStr,"");
//     for (int i = 0; i < (N*N)-1; i++){
//         strcat(stateStr,to_string(state[i]).c_str());
//         // std::cout << to_string(state[i]).c_str() << std::endl;
//     }
//     std::cout << stateStr << std::endl;
//     std::cout << stoull(stateStr) << std::endl;

//     return atoi(stateStr);
// }

string createStateNumberString(int* state){
    char stateStr[30];
    strcpy(stateStr,"");
    for (int i = 0; i < (N*N)-1; i++){
        strcat(stateStr,to_string(state[i]).c_str());
        // std::cout << to_string(state[i]).c_str() << std::endl;
    }
    // std::cout << stateStr << std::endl;

    return stateStr;
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
    // reachedStatesNumbers[createStateNumber(state)] = true;
    reachedStatesStrings[createStateNumberString(state)] = true;
    nbrOfReachedStates++;
}

void printReachedStates() {
    // std::cout << "nbrOfReachedStates: " << nbrOfReachedStates << std::endl;
    // std::cout << "Reached States: " << std::endl;
    // for (int i = 0; i < nbrOfReachedStates; i++){
    //     std::cout << "[";
    //     for (int j = 0; j < nbrOfTiles; j++){
    //         std::cout << reachedStates[i][j];
    //         if (j != nbrOfTiles - 1) {
    //             std::cout << ", ";
    //         }
    //     }
    //     std::cout << "]" << std::endl;
    // }
}

bool checkifReached(int* state){
    string stateNbr = createStateNumberString(state);
    if(reachedStatesStrings.count(stateNbr)) {
            return true;
    }
    return false;
}

//QUEUED STATES
// add state to queue[]. queue[] just stores pointers to arrays in reachedStates[][]
bool addToQueue(int* state) {
    for(int i = 0; i < nbrOfTiles; i++){
        queue[endOfQueue][i] = state[i]; //copy the state
    }
    endOfQueue++;

    // //wrap around if too large
    if(endOfQueue == queueSize - 1) {
        endOfQueue = 0;
        // std::cout << "wrapping end" << std::endl;
    }

    if(endOfQueue == frontOfQueue) {
        std::cout << "Overflow!" << std::endl;
        return false;
    }

    int queueLength = (queueSize + (endOfQueue - frontOfQueue) + 1 ) % queueSize;
    if(queueLength > maxSizeOfQueue) {
        maxSizeOfQueue = queueLength;
    }
    return true;
}

//return the first pointer in the queue, moves the front of the queue forward
int* getFirstFromQueue() {
    if (endOfQueue == frontOfQueue) {
        std::cout << "queue length equal to 0! Can't shift" << std::endl;
        return nullptr;
    }
    if (endOfQueue > queueSize) {
        std::cout << "queue overflow! Can't shift" << std::endl;
        return nullptr;
    }
    int* ptrToFirst = &queue[frontOfQueue][0];
    frontOfQueue++;
    //wrap around if too large
    if(frontOfQueue == queueSize - 1) {
        frontOfQueue = 0;
        // std::cout << "wrapping front" << std::endl;
    }
    return ptrToFirst;
}

void printQueue() {
    // std::cout << "QueueLength: " << endOfQueue - frontOfQueue << std::endl;
    // std::cout << "Queue: " << std::endl;
    // for (int i = frontOfQueue; i < endOfQueue; i++){
    //     int* ptrToState = &queue[i][0];
    //     printState(ptrToState);
    // }
    // std::cout << endl;
    std::cout << "printQueue() is deprecated" << endl;
}

bool checkIfGoalReached(int* statePtr) {
    // I tried to use the stateNbr like with the reached states but its not much faster than to just check each element. It could be helpful if there were many goal states
    string stateNbr = createStateNumberString(statePtr);
    static string xGNbr = createStateNumberString(xG);
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
    std::cout << "no zero position" << std::endl;
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
    if(endOfQueue == frontOfQueue) {
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

    int xprimes[4][nbrOfTiles];
    int nbrOfNewStates = returnxprime(firstState, &xprimes[0][0]);
    for(int i = 0; i < nbrOfNewStates; i++){
        // print("xprime:",xprime)
        if (!checkifReached(&xprimes[i][0])){
            addReachedState(&xprimes[i][0]);
            addToQueue(&xprimes[i][0]);
            if (nbrOfReachedStates%100000 == 0){
                std::cout << "Reached: " << nbrOfReachedStates << std::endl;
                std::cout << "maxSizeOfQueue:" << maxSizeOfQueue << "\t" << ((float)maxSizeOfQueue/queueSize)*100.0 << "%" << std::endl;
                printState(&xprimes[i][0]);
                std::cout << "\n" << std::endl;
            }
        }
    }
}

int main(){
    std::cout << "Beginning!" << std::endl;
    addReachedState(xi);
    addToQueue(xi);
    std::cout << createStateNumberString(xi) << std::endl;

    std::chrono::steady_clock::time_point t1 = high_resolution_clock::now();
    while ((endOfQueue != frontOfQueue) && !goalReached){
        // std::cout << "Press Enter to continue" << std::endl;
        // getchar();
        step();
        // printQueue();
    }
    if ((endOfQueue - frontOfQueue) == 0) {
        std::cout << "Queue is empty" << std::endl;
    }

    std::chrono::steady_clock::time_point t2 = high_resolution_clock::now();
    std::chrono::duration<long long, std::ratio<1, 1000> > ms_int = duration_cast<milliseconds>(t2 - t1);

    std::cout << "Total time: " << round((ms_int.count()/1000)/60) << " min, " <<  round(((ms_int.count()/1000))%60)<< " secs, " << round(ms_int.count()%1000) << " ms" << std::endl;
    std::cout << "Reached: ";
    std::cout << nbrOfReachedStates;
    std::cout << " states"; std::cout<<"\n";

    std::cout << "maxSizeOfQueue:" << maxSizeOfQueue << std::endl;
}