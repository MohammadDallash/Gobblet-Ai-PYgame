#include <iostream>
#include <vector>
using namespace std;

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;


#define fori(size) for(int i=0; i < (size); i++)
#define forj(size) for(int j=0; j < (size); j+= 1)





struct State
{
    // Integer called turn
    int turn;

    // 2D array of size BOARD_SIZE*BOARD_SIZE called board
    int board[BOARD_SIZE][BOARD_SIZE];

    // 2D array of size NUMBER_OF_PLAYERS*INVENTORY_SIZE
    int inventory[NUMBER_OF_PLAYERS][INVENTORY_SIZE];

    // Using std::string for lastMove
    string lastMove = "None";
};






void debug_state(State state)
{
    cout << "Turn: " << state.turn << "\n\n";

    cout << "Board:" << '\n';

    fori(BOARD_SIZE)
    {
        forj(BOARD_SIZE)
        {
            cout << state.board[i][j] << " ";
        }
        cout << endl;
    }

    cout << "\nInventory:\n";
    fori(NUMBER_OF_PLAYERS)
    {
        forj(INVENTORY_SIZE)
        {
            cout << state.inventory[i][j] << " ";
        }
        cout << '\n';
    }
    cout << '\n';

    cout << "Last Move: " << state.lastMove << "\n\n";
}




vector<State> generate_possible_states(State curState)
{
    return {curState, curState, curState,curState,curState}; //TODO (should be the possible states )
}




int static_evaluation (State curState)
{
    return  100; //TODO (should be the static evaluation )
}


//TODO ___ minMax (State curState)



int main()
{
    State initial_state;

    // Input the turn
    cin >> initial_state.turn;

    // Input the board
    for(int i = 0; i < BOARD_SIZE; i++)
    {
        for(int j = 0; j < BOARD_SIZE; j++)
        {
            cin >> initial_state.board[i][j];
        }
    }

    // Input the inventory
    for(int i = 0; i < NUMBER_OF_PLAYERS; i++)
    {
        for(int j = 0; j < INVENTORY_SIZE; j++)
        {
            cin >> initial_state.inventory[i][j];
        }
    }


    debug_state(initial_state);
   
    return 0;
}
