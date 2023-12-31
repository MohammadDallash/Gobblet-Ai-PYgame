#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;

const int EMPTY_TILE = 0;
const int BLACK_SMALL = 1;
const int BLACK_MEDIUM = 2;
const int BLACK_LARGE = 4;
const int BLACK_XLARGE = 8;
const int ALL_BLACK = 15;

const int WHITE_SMALL = 16;
const int WHITE_MEDIUM = 32;
const int WHITE_LARGE = 64;
const int WHITE_XLARGE = 128;
const int ALL_WHITE = 240;

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


int get_highest_multiple_of_2(int n){
    if (n == 0)return 0;
    int bit = 0;
    n >>=1;

    while(n!=0){
        n >>=1;
        bit+=1;
    }
        
    return 1<<bit;
}

int get_largest_piece(int n){

    int pieces[] = {BLACK_XLARGE,WHITE_XLARGE,
                BLACK_LARGE,WHITE_LARGE,
                BLACK_MEDIUM,WHITE_MEDIUM,
                BLACK_SMALL,WHITE_SMALL};
    
    for(int i = 0; i<8; i++){

        if(pieces[i] & n)return pieces[i];
    }
             
    return 0;

}



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



//black is maximizer, white is minimizer
//the sign of the return value determines which is closer to winning
//the value determines how close to winning

//if the returned number is +ve then black is closer to winning
//if the returned number is -ve then white is closer to winning
//the higher the positive number the closer is black to winning
//the lower the negative number the closer is white to winning

//if the return value is 4 then black won, if it is -4 then white won
//if the return value is 0 then no one has an advantage on the other (draw)

//example: if return value is 3 then black is closer to winning and he is one piece away from winning
//example: if return value is -2 then white is closer to winning and he is two pieces away from winning

int static_evaluation (State curState)
{
    //black[0--3] contain the number of black pieces in rows[0--3]
    //black[4--7] contain the number of black pieces in columns[0--3]
    //black[8] contain the number of black pieces in main diagonal
    //black[9] contain the number of black pieces in other diagonal

    //same for white
    vector<int>black(10,0);
    vector<int>white(10,0);
    
    
    //rows
    for(int i = 0; i<4; i++){
        
        for(int j = 0; j<4; j++){

            if(get_largest_piece(curState.board[i][j]) > 15 and curState.board[i][j] != 0)white[i]++;
            if(get_largest_piece(curState.board[i][j]) < 16 and curState.board[i][j] != 0)black[i]++;
        }
    
    }

    //columns
    for(int i = 0; i<4; i++){
        
        for(int j = 0; j<4; j++){

            if(get_largest_piece(curState.board[j][i]) > 15 and curState.board[j][i] != 0)white[i+4]++;
            if(get_largest_piece(curState.board[j][i]) < 16 and curState.board[j][i] != 0)black[i+4]++;

        }

    }


    //main diagonal
    for(int i = 0; i<4; i++){
        if(get_largest_piece(curState.board[i][i]) > 15 and curState.board[i][i] != 0)white[8]++;
        if(get_largest_piece(curState.board[i][i]) < 16 and curState.board[i][i] != 0)black[8]++;
    }



    //other diagonal
    for(int i = 0; i<4; i++){
        if(get_largest_piece(curState.board[i][3-i]) > 15 and curState.board[i][3-i] != 0)white[9]++;
        if(get_largest_piece(curState.board[i][3-i]) < 16 and curState.board[i][3-i] != 0)black[9]++;
    }

    //sort to get max number from each
    sort(white.begin(),white.end());
    sort(black.begin(),black.end());

    //in case white won
    if(white[9] == 4)return white[9]*-1;
    //in case black won
    else if (black[9] == 4)return black[9];

    //in case neither has won (return the closer to winning)
    else{
        
        if(white[9] != black[9]){

            if (white[9] > black[9])return white[9]*-1;

            else return black[9];
        }

        else return 0;
    }

}


//TODO ___ minMax (State curState)

State minMax (State postion ,int depth, int Max)
{
    State temp;
    vector<State> childs_States =generate_possible_states(postion);

    if(depth==0) return postion;
    if(Max) 
    {
        int maxEval=INT32_MIN;
        for(int i=0;i<childs_States.size();i++)
        {
            State eval =minMax (childs_States[i], depth-1, Max);
            int maxEval =max(static_evaluation(eval), maxEval);
            if(static_evaluation(eval)>maxEval) temp=eval;
        }
    } 
    else
    {
        int Eval=INT32_MAX;
        for(int i=0;i<childs_States.size();i++)
        {
            State eval =minMax (childs_States[i], depth-1, Max);
            int minEval =min(static_evaluation(eval), minEval);
            if(static_evaluation(eval)<minEval) temp=eval;
        }
    }
    return temp;

}

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
