
### Right move
Lets assume that the state is 
[3, 4, 7, 2, 8, 6, 1, 0, 5] or graphically,
[3, 4, 7,
 2, 8, 6,
 1, 0, 5]

 A right move would give,
 [3, 4, 7,
 2, 8, 6,
 1, 5, 0] or
 [3, 4, 7, 2, 8, 6, 1, 5, 0]

given that 0 is index 7, we swap x[7] <=> x[8] or 
x[i] <=> x[i+1] where i is the index of 0

### Left move
Lets assume that the state is 
[3, 4, 7, 2, 8, 6, 1, 0, 5] or graphically,
[3, 4, 7,
 2, 8, 6,
 1, 0, 5]

 A left move would give,
 [3, 4, 7,
  2, 8, 6,
  0, 1, 5] or
 [3, 4, 7, 2, 8, 6, 0, 1, 5]

given that 0 is index 7, we swap x[7] <=> x[6] or 
x[i] <=> x[i-1] where i is the index of 0

### Top move
Lets assume that the state is 
[3, 4, 7, 2, 0, 6, 1, 8, 5] or graphically,
[3, 4, 7,
 2, 0, 6,
 1, 8, 5]

 A top move would give,
 [3, 0, 7,
  2, 4, 6,
  1, 8, 5] or
 [3, 0, 7, 2, 4, 6, 1, 8, 5]

given that 0 is index 4, we swap x[4] <=> x[1] or 
x[i] <=> x[i-N] where i is the index of 0

### Bottom move
Lets assume that the state is 
[3, 4, 7, 2, 0, 6, 1, 8, 5] or graphically,
[3, 4, 7,
 2, 0, 6,
 1, 8, 5]

 A top move would give,
 [3, 4, 7,
  2, 8, 6,
  1, 0, 5] or
 [3, 4, 7, 2, 8, 6, 1, 0, 5]

given that 0 is index 4, we swap x[4] <=> x[7] or 
x[i] <=> x[i+N] where i is the index of 0