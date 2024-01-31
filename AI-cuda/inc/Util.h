#ifndef _UTIL_H_
#define _UTIL_H_

#include "State.h"
#include "Constant.h"
#include <algorithm>


int get_largest_piece(int n);
bool checkWins(State s);
int get_largest_piece_size(int n);
void debug_state(State state);
int static_evaluation(State curState);
bool customSort( State a,  State b);
void generate_possible_states(State curState, bool sorting,  int &n_child, State* &a);






#endif