#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <unordered_set>
#include <climits>

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

#define fori(size) for (int i = 0; i < (size); i++)
#define forj(size) for (int j = 0; j < (size); j++)

const int INVENTORY_MOVE = 0;
const int BOARD_MOVE = 1;


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
    vector<int> lastMove[2];
};



int get_largest_piece(int n)
{
    int pieces[] = {BLACK_XLARGE, WHITE_XLARGE,
                    BLACK_LARGE, WHITE_LARGE,
                    BLACK_MEDIUM, WHITE_MEDIUM,
                    BLACK_SMALL, WHITE_SMALL};

    for (int i = 0; i < 8; i++)
    {
        if (pieces[i] & n)
            return pieces[i];
    }

    return 0;
}
bool checkWins(State s) {
    int black = 0;
    int white = 0;

    // Check rows
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (get_largest_piece(s.board[i][j]) > ALL_BLACK && s.board[i][j] != EMPTY_TILE) {
                white++;
            } else if (get_largest_piece(s.board[i][j]) < WHITE_SMALL && s.board[i][j] != EMPTY_TILE) {
                black++;
            }
        }

        if (white == 4) {
                   return true;

        } else if (black == 4) {
                    return true;

        }

        // Reset counters
        black = 0;
        white = 0;
    }

    // Check columns
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (get_largest_piece(s.board[j][i]) > ALL_BLACK && s.board[j][i] != EMPTY_TILE) {
                white++;
            } else if (get_largest_piece(s.board[j][i]) < WHITE_SMALL && s.board[j][i] != EMPTY_TILE) {
                black++;
            }
        }

        if (white == 4) {
            return true;
        } else if (black == 4) {
            return true;
        }

        // Reset counters
        black = 0;
        white = 0;
    }

    // Main diagonal
    for (int i = 0; i < 4; ++i) {
        if (get_largest_piece(s.board[i][i]) > ALL_BLACK && s.board[i][i] != EMPTY_TILE) {
            white++;
        } else if (get_largest_piece(s.board[i][i]) < WHITE_SMALL && s.board[i][i] != EMPTY_TILE) {
            black++;
        }
    }

    if (white == 4) {
        return true;
    } else if (black == 4) {
        return true;
    }

    // Reset counters
    black = 0;
    white = 0;

    // Other diagonal
    for (int i = 0; i < 4; ++i) {
        if (get_largest_piece(s.board[i][3 - i]) > ALL_BLACK && s.board[i][3 - i] != EMPTY_TILE) {
            white++;
        } else if (get_largest_piece(s.board[i][3 - i]) < WHITE_SMALL && s.board[i][3 - i] != EMPTY_TILE) {
            black++;
        }
    }

    if (white == 4) {
        return true;
    } else if (black == 4) {
        return true;
    }

    return false;
}


int get_largest_piece_size(int n)
{
    int pieces[] = {BLACK_XLARGE, WHITE_XLARGE,
                    BLACK_LARGE, WHITE_LARGE,
                    BLACK_MEDIUM, WHITE_MEDIUM,
                    BLACK_SMALL, WHITE_SMALL};

    for (int i = 0; i < 8; i++)
    {
        if (pieces[i] & n)
            return 4 - i / 2; // return size only (color does NOT matter)
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

    cout << "Last Move: \n\n";

    fori(2)
    {
        forj(INVENTORY_SIZE)
        {
            cout << state.lastMove[i][j] << " ";
        }
        cout << '\n';
    }
}

// black is maximizer, white is minimizer
// the sign of the return value determines which is closer to winning
// the value determines how close to winning

// if the returned number is +ve then black is closer to winning
// if the returned number is -ve then white is closer to winning
// the higher the positive number the closer is black to winning
// the lower the negative number the closer is white to winning

//hueristics:
//1- number of white/black pieces in each row/column/diagonal
//2- size of each piece in each row/column/diagonal
int static_evaluation(State curState)
{
    // scores for each row, column, diagonal.
    vector<int> row(4, 0);
    vector<int> column(4, 0);
    int main_diagonal = 0;
    int other_diagonal = 0;


    // calculate the score of each row.
    for (int i = 0; i < 4; i++)
    {
        int black = 0;
        int white = 0;

        for (int j = 0; j < 4; j++)
        {
            // if the piece is white and not an empty tile.
            if (get_largest_piece(curState.board[i][j]) > ALL_BLACK and curState.board[i][j] != EMPTY_TILE){
                white--; // its a white piece
                white-=get_largest_piece_size(curState.board[i][j]); // also add its size
            }

            // if the piece is white black and not an empty tile.
            if (get_largest_piece(curState.board[i][j]) < WHITE_SMALL and curState.board[i][j] != EMPTY_TILE){
                black++; // its a black piece
                black+=get_largest_piece_size(curState.board[i][j]); // also add its size
            }
        }

        row[i] = black + white;
    }

    // columns
    for (int i = 0; i < 4; i++)
    {
        int black = 0;
        int white = 0;

        for (int j = 0; j < 4; j++)
        {

            if (get_largest_piece(curState.board[j][i]) > ALL_BLACK and curState.board[j][i] != EMPTY_TILE){
                white--; // its a white piece
                white-=get_largest_piece_size(curState.board[j][i]); // also add its size
            }

            if (get_largest_piece(curState.board[j][i]) < WHITE_SMALL and curState.board[j][i] != EMPTY_TILE){
                black++; // its a black piece
                black+=get_largest_piece_size(curState.board[j][i]); // also add its size
            }
        }

        column[i] = black + white;
    }


    int black = 0;
    int white = 0;

    // main diagonal
    for (int i = 0; i < 4; i++)
    {
        if (get_largest_piece(curState.board[i][i]) > 15 and curState.board[i][i] != 0){
            white--; // its a white piece
            white-=get_largest_piece_size(curState.board[i][i]); // also add its size

        }

        if (get_largest_piece(curState.board[i][i]) < 16 and curState.board[i][i] != 0){
            black++; // its a black piece
            black+=get_largest_piece_size(curState.board[i][i]); // also add its size
        }

    }

    main_diagonal = black + white;

    black = 0;
    white = 0;

    // other diagonal
    for (int i = 0; i < 4; i++)
    {
        if (get_largest_piece(curState.board[i][3 - i]) > ALL_BLACK and curState.board[i][3 - i] != EMPTY_TILE){
            white--; // its a white piece
            white -= get_largest_piece_size(curState.board[i][3 - i]); // also add its size
        }

        if (get_largest_piece(curState.board[i][3 - i]) < WHITE_SMALL and curState.board[i][3 - i] != EMPTY_TILE){
            black++; // its a black piece
            black += get_largest_piece_size(curState.board[i][3 - i]); // also add its size
        }

    }
    other_diagonal = black + white;


    // calculate the maximum - minimum
    int maxx = INT_MIN, minn = INT_MAX;

    fori(4)
    {
        maxx = max(row[i],maxx);
        minn = min(row[i],minn);

        maxx = max(column[i],maxx);
        minn = min(column[i],minn);
    }
    maxx = max(max(other_diagonal,main_diagonal),maxx);
    minn = min(min(other_diagonal,main_diagonal),minn);


    return maxx + minn +rand()%2;


}

bool customSort(const pair<int, State>& a, pair<int, State>& b) {
            
            return a.first < b.first;
        
        }

//
vector<State> generate_possible_states(State curState)
{
    std::vector<std::pair<int, State>> evaluated_states;

    if (checkWins(curState)) return { curState};
    vector<State> possible_outcome_states; // Initialize vector with 5 copies of curState

    //  locations where each size exists (in the board and the inventory)
    vector<vector<vector<int>>> possible_destination(5);

    // add each location to its corresponding size

    fori(BOARD_SIZE)
    {
        forj(BOARD_SIZE)
        {
            int size = get_largest_piece_size(curState.board[i][j]);

            possible_destination[size].push_back({BOARD_MOVE, i, j});
        }
    }

    fori(BOARD_SIZE)
    {
        forj(BOARD_SIZE)
        {
            int curPiece = curState.board[i][j];

            int size = get_largest_piece_size(curPiece);
            int largest_piece = get_largest_piece(curPiece);

            if (((largest_piece > ALL_BLACK)) ^ (curState.turn))
                continue; // if its not your turn

            for (int s = 0; s < size; s++)
            {
                for (auto dest : possible_destination[s])
                {

                    State newState = curState;

                    newState.board[dest[1]][dest[2]] |= largest_piece;
                    newState.board[i][j] &= ~(largest_piece);

                    newState.lastMove[0] = {BOARD_MOVE, i, j};
                    newState.lastMove[1] = dest;

                    newState.turn = curState.turn ^ 1;

                    possible_outcome_states.push_back(newState);
                }
            }
        }
    }

    unordered_set<int> is_calculated_inventory;

    fori(INVENTORY_SIZE)
    {
        int curPiece = curState.inventory[curState.turn][i];

        int size = get_largest_piece_size(curPiece);
        int largest_piece = get_largest_piece(curPiece);

        if (is_calculated_inventory.find(largest_piece) == is_calculated_inventory.end())
            is_calculated_inventory.insert(largest_piece);

        else
            continue;

        for (int s = 0; s < size; s++)
        {
            for (auto dest : possible_destination[s])
            {
                State newState = curState;

                newState.board[dest[1]][dest[2]] |= largest_piece;

                newState.inventory[curState.turn][i] &= ~(largest_piece);

                newState.lastMove[0] = {INVENTORY_MOVE, curState.turn, i};
                newState.lastMove[1] = dest;

                newState.turn = curState.turn ^ 1;
                possible_outcome_states.push_back(newState);
            }
        }
    }

    // Precompute evaluations
    for (const auto& state : possible_outcome_states) {
        int eval = static_evaluation(state);
        evaluated_states.emplace_back(eval, state);
    }

    // Sort based on precomputed evaluations
    sort(evaluated_states.begin(), evaluated_states.end(),customSort);

    // Extract the sorted states (if needed)
    for (size_t i = 0; i < evaluated_states.size(); ++i) {
        possible_outcome_states[i] = evaluated_states[i].second;
    }

    return possible_outcome_states;
}



State minMax (State postion ,int depth)
{
    State temp;
    vector<State> childs_States =generate_possible_states(postion);

    if(depth==0) return postion;
    if(postion.turn == 0)
    {
        int largest_Eval=INT32_MIN;
        for(int i=0;i<childs_States.size();i++)
        {
            State largest_state =minMax (childs_States[i], depth-1);

            if((static_evaluation(largest_state))>largest_Eval)
            {
                temp = childs_States[i];
                largest_Eval = static_evaluation(largest_state);
            }
        }
    }
    else
    {
        int minest_Eval=INT32_MAX;
        for(int i=0;i<childs_States.size();i++)
        {
            State minest_state =minMax(childs_States[i], depth-1);
            if(static_evaluation(minest_state)<minest_Eval)
            {
                temp = childs_States[i];
                minest_Eval = static_evaluation(minest_state);
            }
        }
    }
    return temp;
}



State minMax_alph_beta (State postion ,int depth,int alph , int beta)
{ 

    State temp;
    vector<State> childs_States =generate_possible_states(postion);

    if(depth==0) return postion;
    if(postion.turn == 0)//maximizer
    {
        int largest_Eval=INT32_MIN;
        reverse(childs_States.begin(), childs_States.end());
        for(int i=0;i<childs_States.size();i++)
        {
            State largest_state =minMax (childs_States[i], depth-1);
            alph=max(static_evaluation(largest_state),alph);
            if(static_evaluation(largest_state)>largest_Eval)
            {
                temp = childs_States[i];
                largest_Eval = static_evaluation(largest_state);
            }
            if(alph>= beta){
                break;
            }

        }
    }
    else // minimizer
    {
        int minest_Eval=INT32_MAX;
        for(int i=0;i<childs_States.size();i++)
        {
            State minest_state =minMax(childs_States[i], depth-1);
            beta=min(beta,static_evaluation(minest_state));
            if(static_evaluation(minest_state)<minest_Eval)
            {
                temp = childs_States[i];
                minest_Eval = static_evaluation(minest_state);
            }
            if(alph>= beta){
                break;
            }

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
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        for (int j = 0; j < BOARD_SIZE; j++)
        {
            cin >> initial_state.board[i][j];
        }
    }

    // Input the inventory
    for (int i = 0; i < NUMBER_OF_PLAYERS; i++)
    {
        for (int j = 0; j < INVENTORY_SIZE; j++)
        {
            cin >> initial_state.inventory[i][j];
        }
    }

    // debug_state(initial_state);
    auto state =  minMax_alph_beta(initial_state,3,INT32_MIN,INT32_MAX);

    cout << state.turn << " ";



    fori(BOARD_SIZE)
    {
        forj(BOARD_SIZE)
        {
            cout << state.board[i][j] << " ";
        }
    }


    fori(NUMBER_OF_PLAYERS)
    {
        forj(INVENTORY_SIZE)
        {
            cout << state.inventory[i][j] << " ";
        }
 
    }
    return 0;
}
