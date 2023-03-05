
let nbrOfSquares = 9;
let tileSize;
let rectanglePositions;

let tiles = []; //holds tiles in order they appear

let tilePositions = []; //x and y pairs for each tile position

function setup() {
    createCanvas(600, 600);
    tileSize = height/sqrt(nbrOfSquares);

    for (let i = 0; i < nbrOfSquares; i++) {
        xpos = i%sqrt(nbrOfSquares);
        ypos = floor(i/sqrt(nbrOfSquares));
        tilePositions[i] = new Position(xpos*tileSize,ypos*tileSize);
        tiles[i] = new tile(i);
    }
    print(tilePositions);
  
    background(0);
    drawTiles();
}

function draw() {
    background(0);
    drawTiles();
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
            rectMode(CORNER);
            rect(this.xPos, this.yPos, tileSize, tileSize);
            stroke(0);fill(0);
            textSize(50);
            textAlign(CENTER, CENTER);
            text(String(this.number),this.xPos+ tileSize/2,this.yPos+ tileSize/2)
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
                print("no position found")
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
        print("left");
        for (i in tiles) {
            // if (tiles[i].number == 0 && i%nbrOfSquares != nbrOfSquares-1) {
            if (tiles[i].number == 0) {
                print(i)
                temp = tiles[i+1]
                tiles[i+1] = tiles[i]
                tiles[i] = temp
            } 
        }
    } else if (keyCode === RIGHT_ARROW) {
      print("right");
    } else if (keyCode === UP_ARROW) {
        print("up");
    } else if (keyCode === DOWN_ARROW) {
        print("down");
      }
}


  