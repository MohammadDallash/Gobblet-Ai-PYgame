#ifndef _UTIL_H_
#define _UTIL_H_

#include "State.h"
#include "Constant.h"
#include "unordered_map"
#include "unordered_set"
#include <algorithm>


int get_largest_piece(int n);
bool checkWins(State s);
int get_largest_piece_size(int n);
void debug_state(State state);
int static_evaluation(State curState);
bool customSort( State a,  State b);
vector<State> generate_possible_states(State curState, bool sorting);



#endif