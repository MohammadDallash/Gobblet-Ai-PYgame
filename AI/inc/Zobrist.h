#ifndef _ZOBRIST_H_
#define _ZOBRIST_H_

#include <random>
extern unsigned long long zobTable[4][4][8];
void fill_table();
int indexing(int piece);
int32_t get_largest_piecee(int n);
unsigned long long computeHash(int board[][4], int turn);

#endif