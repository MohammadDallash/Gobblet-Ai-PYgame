#include <ctime> 
#include <iostream>
#include <string>
#include <algorithm>
#include <cstdint>
#include <climits>
#include <random>
#include "State.h"
#include "Constant.h"
#include "Util.h"


using namespace std;
int difficulty;

int MXchild = 25;


State minMax_alpha_beta (State postion ,int depth,int alpha , int beta, bool buring, bool mutation)
{ 
    int evl;
    State temp;
    int n_child = 0;
    State * a;
    generate_possible_states(postion, buring &&(difficulty!=1) ,n_child ,a);


    if(depth==0) return postion;
    if(postion.turn == 0)//maximizer
    {
        int largest_Eval=INT32_MIN;
        reverse(a,a + n_child );
        for(int i=0;i<n_child;i++)
        {  
            State largest_state =minMax_alpha_beta (a[i], depth-1,alpha,beta, buring, mutation);
            evl=largest_state.static_evl;
            alpha=max(evl,alpha);
            if(evl>largest_Eval or (evl== largest_Eval and mutation and rand()%3 == 1))
            {
                temp = a[i];
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
        for(int i=0;i<n_child;i++)
        {
  
            State minest_state =minMax_alpha_beta(a[i], depth-1,alpha,beta, buring, mutation);
            evl=minest_state.static_evl;
            beta=min(beta,evl);

            if(evl<minest_Eval or (evl== minest_Eval and mutation and rand()%3 == 1))
            {
                temp = a[i];
                minest_Eval = evl;
            }

            if(alpha>= beta and buring){
                break;
            }
            
        }
    }

    free(a);
    return temp;
}

int main(int argc, char *argv[]) 
{
    // fill_table();

    srand(static_cast<unsigned int>(time(0)));
    State initial_state;

    // Input the turn.
    initial_state.turn = atoi(argv[1]);

    // Input the board.
    int arg_index = 2;
    fori(BOARD_SIZE) {
        forj(BOARD_SIZE) {
            initial_state.board[i][j] = atoi(argv[arg_index++]);
        }
    }

    // Input the inventory.
    fori(NUMBER_OF_PLAYERS) {
        forj(INVENTORY_SIZE) {
            initial_state.inventory[i][j] = atoi(argv[arg_index++]);
        }
    }


    difficulty = atoi(argv[arg_index]);
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

    cout << endl;

    // print destination values.
    fori(3) cout << best_state.lastMove[1][i] << " ";

    return 0;
}

