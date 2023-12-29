#include <iostream>
#include <vector>
#include <string>


using namespace std;

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;


#define fori(size) for(int i=0; i < (size); i++)
#define forj(size) for(int j=0; j < (size); j++)





struct State
{
    // Integer called turn
    int turn;

    // 2D array of size BOARD_SIZE*BOARD_SIZE called board
    int board[BOARD_SIZE][BOARD_SIZE];

    // 2D array of size NUMBER_OF_PLAYERS*INVENTORY_SIZE
    int inventory[NUMBER_OF_PLAYERS][INVENTORY_SIZE];

    // Using std::string for lastMove
    string lastMove;
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
    vector<State> possibleStates(5, curState); // Initialize vector with 5 copies of curState
    return possibleStates;
}



//if curState doesnt have a winner it will return 0
//if black is the winner in curState it will return +5
//if white is the winner in curState it will return -5
//therefore black is the maximizer abd white is the minimizer
int static_evaluation (State curState)
{
    //create 3 loops that checks for a winner in each row, column, diagonal.
    //counters for each color
    int black = 0;
    int white = 0;

    //rows
    for(int i = 0; i<4; i++){
        
        for(int j = 0; j<4; i++){

            if(curState.board[i][j] > 15 and curState.board[i][j] != 0)white++;
            if(curState.board[i][j] < 16 and curState.board[i][j] != 0)black++;
        }
    
        if(white == 4)return -5;
        else if(black == 4)return 5;

        //reset counters.
        black = 0;
        white = 0;
    }

    //columns
    for(int i = 0; i<4; i++){
        
        for(int j = 0; j<4; i++){

            if(curState.board[j][i] > 15 and curState.board[i][j] != 0)white++;
            if(curState.board[j][i] < 16 and curState.board[i][j] != 0)black++;

        }

        if(white == 4)return -5;
        else if(black == 4)return 5;

        //reset counters.
        black = 0;
        white = 0;
    }


    //main diagonal
    for(int i = 0; i<4; i++){
        if(curState.board[i][i] > 15 and curState.board[i][i] != 0)white++;
        if(curState.board[i][i] < 16 and curState.board[i][i] != 0)black++;
    }

    if(white == 4)return -5;
    else if(black == 4)return 5;

    //reset counters.
    black = 0;
    white = 0;


    //other diagonal
    for(int i = 0; i<4; i++){
        if(curState.board[i][3-i] > 15 and curState.board[i][3-i] != 0)white++;
        if(curState.board[i][3-i] < 16 and curState.board[i][3-i] != 0)black++;
    }

    if(white == 4)return -5;
    else if(black == 4)return 5;

    //in case of no winner
    else return 0;

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


    //debug_state(initial_state);
    cout << static_evaluation(initial_state);
    return 0;
}
