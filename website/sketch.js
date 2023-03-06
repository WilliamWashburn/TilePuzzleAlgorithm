
let nbrOfSquares = 9;
let tileSize;
let rectanglePositions;

let tiles = []; //holds tiles in order they appear

let tilePositions = []; //x and y pairs for each tile position

let goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
let goalReached = false

function setup() {
    createCanvas(600, 600);
    tileSize = height/sqrt(nbrOfSquares);

    for (let i = 0; i < nbrOfSquares; i++) {
        xpos = i%sqrt(nbrOfSquares);
        ypos = floor(i/sqrt(nbrOfSquares));
        tilePositions[i] = new Position(xpos*tileSize,ypos*tileSize);
        tiles[i] = new tile(i);
    }

    shuffleTiles()
    
    print(tilePositions);
    print(tiles);
  
    background(0);
    drawTiles();

    let initialState = []
    for (let i = 0; i < tiles.length; i++) {
        initialState[i] = tiles[i].number
    }

    getSolution(initialState);
}

function getSolution(initialState) {
    const url = 'http://127.0.0.1:5000/solvePuzzle'
    data = {
        "initial-state": initialState
    }
    fetch(url,{
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(result => {
        console.log('Received result:', result);
        // Do something with the result
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

//Fisher-Yates Shuffle https://bost.ocks.org/mike/shuffle/
function shuffleTiles() {
    var m = tiles.length, t, i;
    while (m) {
        i = Math.floor(Math.random() * m--);
        t = tiles[m];
        tiles[m] = tiles[i];
        tiles[i] = t;
        print("shuffling")
    }
}

let waitForKey = true;

function draw() {
    while(waitForKey){
        return 1;
    }
    waitForKey = true;
    print("next State");
    background(0);
    drawTiles();

    checkIfGoalReached()
    if(goalReached){
        whenGoalReached();
    }
}

function drawTiles() {
    for (i in tiles){ 
        tiles[i].drawTile();
    }
}

class tile {
    
    constructor(number) {
        this.number = number;
        this.xPos = 0;
        this.yPos = 0;
    }
    

    drawTile () {
        this.getPosition();
        if (this.number != 0){
            fill(255);
            stroke(255)
            rectMode(CORNER);
            rect(this.xPos, this.yPos, tileSize, tileSize);
            stroke(0);fill(0);
            textSize(50);
            textAlign(CENTER, CENTER);
            text(String(this.number),this.xPos+ tileSize/2,this.yPos+ tileSize/2);
        }
    }

    getPosition() {
        for (i in tiles) {
            if (tiles[i].number == this.number) {
                this.xPos = tilePositions[i].xPos;
                this.yPos = tilePositions[i].yPos;
                return
            }
            if (i == nbrOfSquares) {
                print("no position found");
            }
        }
    }
}

class Position {
    constructor(xPos, yPos){
        this.xPos = xPos;
        this.yPos = yPos;
    }
}

function keyPressed() {
    if (keyCode === LEFT_ARROW) {
        let inx = findZeroTile();
        if(inx%sqrt(nbrOfSquares) != sqrt(nbrOfSquares)-1) {
            print("left");
            waitForKey = false;
            temp = tiles[inx+1];
            tiles[inx+1] = tiles[inx];
            tiles[inx] = temp;
        }
    } else if (keyCode === RIGHT_ARROW) {
        let inx = findZeroTile();
        if(inx%sqrt(nbrOfSquares) != 0) {
            print("right");
            waitForKey = false;
            temp = tiles[inx-1];
            tiles[inx-1] = tiles[inx];
            tiles[inx] = temp;
        }
    } else if (keyCode === UP_ARROW) {
        let inx = findZeroTile();
        if(inx<nbrOfSquares-sqrt(nbrOfSquares)) {
            print("up");
            waitForKey = false;
            temp = tiles[inx+sqrt(nbrOfSquares)];
            tiles[inx+sqrt(nbrOfSquares)] = tiles[inx];
            tiles[inx] = temp;
        }
    } else if (keyCode === DOWN_ARROW) {
        let inx = findZeroTile();
        if(inx>=sqrt(nbrOfSquares)) {
            print("down");
            waitForKey = false;
            temp = tiles[inx-sqrt(nbrOfSquares)];
            tiles[inx-sqrt(nbrOfSquares)] = tiles[inx];
            tiles[inx] = temp;
        }
      }
}

function findZeroTile() {
    let inx;
    for (inx = 0; inx < nbrOfSquares; inx++) {
        if (tiles[inx].number == 0) {
            break;
        }
    }
    return inx
}

function checkIfGoalReached() {
    print("checking");
    for (inx = 0; inx < nbrOfSquares; inx++) {
        if (tiles[inx].number != goalState[inx]) {
            goalReached = false;
            return 0;
        }
    }
    print("goal reached!");
    goalReached = true;
}

function whenGoalReached() {
    fill(0,255,0,50);
    rect(0,0,width,height);
}


  