#ifndef _ZOBRIST_H_
#define _ZOBRIST_H_

#include <random>
void fill_table();
int indexing(int piece);
int32_t get_largest_piecee(int n);
unsigned long long computeHash(int board[][4], int turn);

#endif