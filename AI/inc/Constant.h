#ifndef _CONSTANT_H_
#define _CONSTANT_H_

const int EMPTY_TILE = 0;
const int BLUE_SMALL = 1;
const int BLUE_MEDIUM = 2;
const int BLUE_LARGE = 4;
const int BLUE_XLARGE = 8;
const int ALL_BLUE = 15;

const int RED_SMALL = 16;
const int RED_MEDIUM = 32;
const int RED_LARGE = 64;
const int RED_XLARGE = 128;
const int ALL_RED = 240;

#define fori(size) for (int i = 0; i < (size); i++)
#define forj(size) for (int j = 0; j < (size); j++)
#define fork(size) for (int k = 0; k < (size); k++)
const int INVENTORY_MOVE = 0;
const int BOARD_MOVE = 1;




#endif