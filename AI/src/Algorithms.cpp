#include <ctime> 
#include <iostream>
#include <string>
#include <algorithm>
#include <cstdint>
#include <unordered_set>
#include <climits>
#include <unordered_map>
#include <random>
#include "State.h"
#include "Constant.h"
#include "Util.h"
#include "Zobrist.h"
#include "map"


// gp_hash_table<int, int> table;


using namespace std;
int difficulty;
unsigned long long zobTable[4][4][8];
map<unsigned long long, int> calculated_states;
// gp_hash_table<unsigned long long, int> visited;
int MXchild = 25;


State minMax_alpha_beta (State postion ,int depth,int alpha , int beta, bool buring, bool mutation)
{ 
    int evl;
    State temp;
    vector<State> childs_States = generate_possible_states(postion, buring &&(difficulty!=1) );

    if (difficulty == 1 and childs_States.size() > MXchild)
         childs_States.resize(MXchild);

    if(depth==0) return postion;
    if(postion.turn == 0) //maximizer
    {
        int largest_Eval=INT32_MIN;
        reverse(childs_States.begin(), childs_States.end());
        for(int i=0;i<childs_States.size();i++)
        {  
            State largest_state =minMax_alpha_beta (childs_States[i], depth-1,alpha,beta, buring, mutation);
            evl=largest_state.static_evl;
            alpha=max(evl,alpha);
            if(evl>largest_Eval or (evl== largest_Eval and mutation and rand()%3 == 1))
            {
                temp = childs_States[i];
                largest_Eval = evl;
            }

            if(alpha>= beta and buring){
                break;
            }
        }
    }
    else // minimizer
    {
        
        int minest_Eval=INT32_MAX;
        for(int i=0;i<childs_States.size();i++)
        {
  
            State minest_state = minMax_alpha_beta(childs_States[i], depth-1,alpha,beta, buring, mutation);
            evl=minest_state.static_evl;
            beta=min(beta,evl);

            if(evl<minest_Eval or (evl== minest_Eval and mutation and rand()%3 == 1))
            {
                temp = childs_States[i];
                minest_Eval = evl;
            }

            if(alpha>= beta and buring){
                break;
            }
            
        }
    }
    return temp;
}

int main(int argc, char *argv[]) 
{
    fill_table();
    while(1){

    srand(static_cast<unsigned int>(time(0)));
    State initial_state;

    // Input the turn.
    cin >> initial_state.turn;

    // Input the board.
    int arg_index = 2;
    fori(BOARD_SIZE) {
        forj(BOARD_SIZE) {
          cin >>   initial_state.board[i][j];
        }
    }

    // Input the inventory.
    fori(NUMBER_OF_PLAYERS) {
        forj(INVENTORY_SIZE) {
            cin >>  initial_state.inventory[i][j];
        }
    }


    cin >> difficulty;
    // itr deepening
    State best_state;
    if(initial_state.turn==0) // max
    best_state.static_evl = INT32_MIN;
    else best_state.static_evl = INT32_MAX;


    for(int i = difficulty; i<=difficulty; i++)
    {

    auto state = minMax_alpha_beta(initial_state, i, INT32_MIN, INT32_MAX, true, true);

    if      (state.static_evl > best_state.static_evl && initial_state.turn == 0) best_state = state;
    else if (state.static_evl < best_state.static_evl && initial_state.turn == 1) best_state = state;
    else if (state.static_evl == best_state.static_evl && (rand()%3 == 1) ) best_state = state;
        
    }

    // debug_state(initial_state);

    // print source values.
    fori(3) cout << best_state.lastMove[0][i] << " ";

    // cout << endl;

    // print destination values.
    fori(3) cout << best_state.lastMove[1][i] << " ";
    }

    for (auto x : visited)
    {
        cout << x.first << "    " << x.second << endl;
    }

    return 0;
}

