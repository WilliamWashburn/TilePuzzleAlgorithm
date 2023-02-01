import deadpixel.command.*;

int rectWidth;
int blankTile;

int numberTilesSqrted = 3;
int widthX = 640;
int squarewidth = round(widthX/numberTilesSqrted);

int prevxPos;
int prevyPos;
int xPos;
int yPos;

int addition = 0;
int speed = 50;

boolean drawImage;

//PImage[] images = new PImage[(int)sq(numberTilesSqrted)];
tileImage[] images = new tileImage[(int)sq(numberTilesSqrted)];

tileImage tempImage;
//PImage mainImage;

boolean gameComplete = false;

int moveCount = 0;

void setup() {
  size(640, 640);
  frameRate(30);
  //frameRate(2);

  noStroke();
  background(0);

  images[0] = new tileImage(loadImage("one.png"), 1);
  images[1] = new tileImage(loadImage("two.png"), 2);
  images[2] = new tileImage(loadImage("three.png"), 3);
  images[3] = new tileImage(loadImage("four.png"), 4);
  images[4] = new tileImage(loadImage("five.png"), 5);
  images[5] = new tileImage(loadImage("six.png"), 6);
  images[6] = new tileImage(loadImage("seven.png"), 7);
  images[7] = new tileImage(loadImage("eight.png"), 8);
  //images[8] = new tileImage(loadImage("nine.png"), 9);
  //images[9] = new tileImage(loadImage("ten.png"), 10);
  //images[10] = new tileImage(loadImage("eleven.png"), 11);
  //images[11] = new tileImage(loadImage("twelve.png"), 12);
  //images[12] = new tileImage(loadImage("thirteen.png"), 13);
  //images[13] = new tileImage(loadImage("fourteen.png"), 14);
  //images[14] = new tileImage(loadImage("fifteen.png"), 15);
  shuffle(images, numberTilesSqrted*numberTilesSqrted-1);

  blankTile = round(random(0, sq(numberTilesSqrted)-1));
}

void draw() {
  if (gameComplete) {
    fill(0, 255, 0);
    rectMode(CENTER);
    rect(width/2, height/2, 150, 80);
    textAlign(CENTER, CENTER);
    //textMode(CENTER);
    fill(0);
    textSize(40);
    text("DONE", width/2, height/2);

    fill(255, 0, 0);
    String playCount = "you played: ";
    playCount += moveCount;
    text(playCount, width/2, height/2+70);
  } else {
    background(255);
    drawSquares();
    checkIfDone();
  }
}

void drawSquares() {
  int whichImage = 0;
  //cycle throught images to draw
  for (int i = 0; i < sq(numberTilesSqrted); i++) {
    xPos = squarewidth*(i%numberTilesSqrted);
    yPos = squarewidth*(i/numberTilesSqrted);

    stroke(155);
    fill(0);
    rectMode(CORNER);
    drawImage = true;
    int tolerance = 40;

    //moving Right
    if (movingRight) { //draw motion
      if (i == blankTile + 1) {
        xPos = xPos - squarewidth + addition;
        if (addition >= squarewidth - tolerance) {
          movingRight = false;
          addition = 0;
        }
        addition+=speed;
      }
      if (i == blankTile) {
        drawImage = false;
      }
    }

    //moving Left
    else if (movingLeft) { //draw motion
      if (i == blankTile - 1) {
        xPos = xPos + squarewidth - addition;
        if (addition >= squarewidth - tolerance) {
          movingLeft = false;
          addition = 0;
          //i = 0;
          //whichImage = 0;
        }
        addition+=speed;
      }
      if (i == blankTile - 1) {
        drawImage = false;
      }
    }

    //moving Down
    else if (movingDown) { //draw motion
      if (i == blankTile + numberTilesSqrted) {
        yPos = yPos - squarewidth + addition;
        if (addition >= squarewidth - tolerance) {
          movingDown = false;
          addition = 0;
        }
        addition+=speed;
      }
      if (i == blankTile + numberTilesSqrted) {
        drawImage = false;
      }
    }

    //moving UP
    else if (movingUp) { //draw motion
      if (i == blankTile - numberTilesSqrted) {
        yPos = yPos + squarewidth - addition;
        if (addition >= squarewidth - tolerance) {
          movingUp = false;
          addition = 0;
        }
        addition+=speed;
      }
      if (i == blankTile - numberTilesSqrted) {
        drawImage = false;
      }
    }


    //if (!movingUp && !movingDown && !movingRight && !movingLeft) {
    //}

    if (i != blankTile) {
      image(images[whichImage].image, xPos, yPos, squarewidth, squarewidth);
      whichImage++;
    }

    //movingRight = false;
    //movingLeft = false;
    //movingUp = false;
    //movingDown = false;
  }
}

void drawGrid() {
  stroke(155);
  for (int i = 0; i < squarewidth*numberTilesSqrted; i = i + squarewidth) {
    line(i, 0, i, height);
  }
  for (int i = 0; i < squarewidth*numberTilesSqrted; i = i + squarewidth) {
    line(0, i, width, i);
  }
}

void keyPressed() {
  if (movingRight || movingLeft || movingUp || movingDown) {
  } else {
    if (key == ENTER) {
      print("hello");
      Runtime.getRuntime().exec("touch hello.py");
    }
    if (key == CODED) {
      if (keyCode == UP) {
        moveUpTile();
      } else if (keyCode == DOWN) {
        moveDownTile();
      } else if (keyCode == RIGHT) {
        moveRightTile();
      } else if (keyCode == LEFT) {
        moveLeftTile();
      }
    }
  }
}

boolean movingRight = false;
boolean movingLeft = false;
boolean movingUp = false;
boolean movingDown = false;

void moveRightTile() {
  //println("RIGHT!");
  //is move legal?
  int oldRow = blankTile / numberTilesSqrted;
  int newTile = blankTile - 1;
  int newRow = newTile / numberTilesSqrted;
  if (oldRow != newRow || newTile < 0) {
    println("cant move right");
  } else {
    moveCount++;
    movingRight = true;
    blankTile = newTile;
    //println(blankTile);
  }
  //printNumberOrder();
}

void moveLeftTile() {
  //println("LEFT!");
  int oldRow = blankTile / numberTilesSqrted;
  int newTile = blankTile + 1;
  int newRow = newTile / numberTilesSqrted;
  if (oldRow != newRow ) {
    println("cant move left");
  } else {
    moveCount++;
    movingLeft = true;
    blankTile = newTile;
    //println(blankTile);
  }
  //printNumberOrder();
}

void moveDownTile() {
  //println("DOWN!");
  int newTile = blankTile - numberTilesSqrted;
  //println(newTile);
  if (newTile < 0) {
    println("cant move down");
  } else {
    moveCount++;
    movingDown = true;
    blankTile = newTile;
    //println(blankTile);
    moveImageDown(blankTile);
  }
  //printNumberOrder();
}

void moveUpTile() {
  //println("UP!");
  int newTile = blankTile + numberTilesSqrted;
  //println(newTile);
  if (newTile >= sq(numberTilesSqrted)) {
    println("cant move up");
  } else {
    moveCount++;
    movingUp = true;
    blankTile = newTile;
    //println(blankTile);
    moveImageUp(blankTile);
  }
  //printNumberOrder();
}

void moveImageDown(int nmbToMove) {
  // 1 is nmbToMove
  //we have 1 8 7 3 4
  //we want 1 7 3 8 4
  print(nmbToMove);
  tempImage = images[nmbToMove];
  images[nmbToMove] = images[nmbToMove+1];
  images[nmbToMove+1] = images[nmbToMove+2];
  images[nmbToMove+2] = tempImage;
  //for (int i = 0; i < numberTilesSqrted ; i++) {
  //  images[nmbToMove + i] = images[nmbToMove+i+1];
  //}
  //images[nmbToMove+numberTilesSqrted-1] = tempImage;
}

void moveImageUp(int nmbToMove) {
  //tempImage = images[nmbToMove - 1];
  //for (int i = 1; i < numberTilesSqrted ; i++) {
  //  images[nmbToMove - i] = images[nmbToMove-i-1];
  //}
  //images[nmbToMove-numberTilesSqrted] = tempImage;
  tempImage = images[nmbToMove - 1];
  images[nmbToMove-1] = images[nmbToMove-2];
  images[nmbToMove-2] = images[nmbToMove-3];
  images[nmbToMove-3] = tempImage;
}

void shuffle(tileImage images[], int nbr) {
  for (int i = nbr - 1; i > 0; i--) {
    int inx = (int)random(0, nbr);
    tileImage temp = images[inx];
    images[inx] = images[i];
    images[i] = temp;
  }
}

void printNumberOrder() {
  for (int i = 0; i < sq(numberTilesSqrted)-1; i++) {
    print(images[i].number);
  }
  println();
}

void checkIfDone() {
  boolean done = true;
  if (images[0].number != 1) {
    done = false;
  } else if (images[1].number != 2) {
    done = false;
  } else if (images[2].number != 3) {
    done = false;
  } else if (images[3].number != 4) {
    done = false;
  } else if (images[4].number != 5) {
    done = false;
  } else if (images[5].number != 6) {
    done = false;
  } else if (images[6].number != 7) {
    done = false;
  } else if (images[7].number != 8) {
    done = false;
  }
  //else if (images[8].number != 9) {
  //  done = false;
  //} else if (images[9].number != 10) {
  //  done = false;
  //} else if (images[10].number != 11) {
  //  done = false;
  //} else if (images[11].number != 12) {
  //  done = false;
  //} else if (images[12].number != 13) {
  //  done = false;
  //} else if (images[13].number != 14) {
  //  done = false;
  //}

  if (done) {
    print("we are done!");
    gameComplete = true;
  }
}

class tileImage {
  public PImage image;
  public int number;
  tileImage(PImage input_image, int input_number) {
    image = input_image;
    number = input_number;
  }
}
