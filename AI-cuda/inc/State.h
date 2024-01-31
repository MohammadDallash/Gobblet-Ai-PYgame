#ifndef _STATE_H_
#define _STATE_H_

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;

using namespace std;

struct State
{
    // Integer called turn
    int turn;

    // 2D array of size BOARD_SIZE*BOARD_SIZE called board
    int board[BOARD_SIZE][BOARD_SIZE];

    // 2D array of size NUMBER_OF_PLAYERS*INVENTORY_SIZE
    int inventory[NUMBER_OF_PLAYERS][INVENTORY_SIZE];

    /* lastMove[0] = src, lastMove[1] = dest
     *
     * [0,1,1]
     * [0,2,3]
     *
    each of src and dest = [t, i, j]  (t is INVENTORY_MOVE OR BORAD_MOVE)*/
    int lastMove[2][3];
    int static_evl;
};


#endif