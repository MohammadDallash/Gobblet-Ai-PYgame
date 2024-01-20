#include <ctime> 
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <unordered_set>
#include <climits>
#include <unordered_map>
#include <random>

using namespace std;

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;

const int EMPTY_TILE = 0;
const int BLUE_SMALL = 1;
const int BLUE_MEDIUM = 2;
const int BLUE_LARGE = 4;
const int BLUE_XLARGE = 8;
const int ALL_BLUE = 15;

const int RED_SMALL = 16;
const int RED_MEDIUM = 32;
const int RED_LARGE = 64;
const int RED_XLARGE = 128;
const int ALL_RED = 240;

#define fori(size) for (int i = 0; i < (size); i++)
#define forj(size) for (int j = 0; j < (size); j++)
#define fork(size) for (int k = 0; k < (size); k++)
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
    int static_evl;
};
unsigned long long zobTable[4][4][8];

void fill_table()
{
    std::random_device rd;     // Get a random seed from the OS entropy device, or whatever
    std::mt19937_64 eng(rd()); // Use the 64-bit Mersenne Twister 19937 generator
                               // and seed it with entropy.

    // Define the distribution, by default it goes from 0 to MAX(unsigned long long)
    // or what have you.
    std::uniform_int_distribution<unsigned long long> distr;

    fori(4)
    {
        forj(4)
        {
            fork(8)
            {
                zobTable[i][j][k] = distr(eng);
            }
        }
    }
}

int indexing(int piece)
{
    if (piece == BLUE_SMALL)
        return 1;
    if (piece == BLUE_MEDIUM)
        return 2;
    if (piece == BLUE_LARGE)
        return 3;
    if (piece == BLUE_XLARGE)
        return 4;
    if (piece == RED_SMALL)
        return 5;
    if (piece == RED_MEDIUM)
        return 6;
    if (piece == RED_LARGE)
        return 7;
    if (piece == RED_XLARGE)
        return 8;
    else
        return 0;
}

int board[4][4] = {
    {BLUE_MEDIUM, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE},
    {EMPTY_TILE, BLUE_XLARGE, BLUE_LARGE, EMPTY_TILE},
    {EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE},
    {EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE}};

int32_t get_largest_piecee(int n)
{
    vector<int> pieces = {BLUE_XLARGE, RED_XLARGE, BLUE_LARGE, RED_LARGE, BLUE_MEDIUM, RED_MEDIUM, BLUE_SMALL, RED_SMALL};

    for (int piece : pieces)
    {
        if (piece & n)

            return piece;
    }
    return 0;
}

unsigned long long computeHash(int board[][4], int turn)
{
    unsigned long long h = 0;
    fori(4)
    {
        forj(4)
        {
            if (board[i][j] != EMPTY_TILE)
            {
                int piece = indexing(get_largest_piecee(board[i][j]));
                h ^= zobTable[i][j][piece];
            }
        }
    }
    return h + turn;
}




int get_largest_piece(int n)
{
    int pieces[] = {BLUE_XLARGE, RED_XLARGE,
                    BLUE_LARGE, RED_LARGE,
                    BLUE_MEDIUM, RED_MEDIUM,
                    BLUE_SMALL, RED_SMALL};

    for (int i = 0; i < 8; i++)
    {
        if (pieces[i] & n)
            return pieces[i];
    }

    return 0;
}
bool checkWins(State s) {
    int blue = 0;
    int red = 0;

    // Check rows
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (get_largest_piece(s.board[i][j]) > ALL_BLUE && s.board[i][j] != EMPTY_TILE) {
                red++;
            } else if (get_largest_piece(s.board[i][j]) < RED_SMALL && s.board[i][j] != EMPTY_TILE) {
                blue++;
            }
        }

        if (red == 4) {
                   return true;

        } else if (blue == 4) {
                    return true;

        }

        // Reset counters
        blue = 0;
        red = 0;
    }

    // Check columns
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (get_largest_piece(s.board[j][i]) > ALL_BLUE && s.board[j][i] != EMPTY_TILE) {
                red++;
            } else if (get_largest_piece(s.board[j][i]) < RED_SMALL && s.board[j][i] != EMPTY_TILE) {
                blue++;
            }
        }

        if (red == 4) {
            return true;
        } else if (blue == 4) {
            return true;
        }

        // Reset counters
        blue = 0;
        red = 0;
    }

    // Main diagonal
    for (int i = 0; i < 4; ++i) {
        if (get_largest_piece(s.board[i][i]) > ALL_BLUE && s.board[i][i] != EMPTY_TILE) {
            red++;
        } else if (get_largest_piece(s.board[i][i]) < RED_SMALL && s.board[i][i] != EMPTY_TILE) {
            blue++;
        }
    }

    if (red == 4) {
        return true;
    } else if (blue == 4) {
        return true;
    }

    // Reset counters
    blue = 0;
    red = 0;

    // Other diagonal
    for (int i = 0; i < 4; ++i) {
        if (get_largest_piece(s.board[i][3 - i]) > ALL_BLUE && s.board[i][3 - i] != EMPTY_TILE) {
            red++;
        } else if (get_largest_piece(s.board[i][3 - i]) < RED_SMALL && s.board[i][3 - i] != EMPTY_TILE) {
            blue++;
        }
    }

    if (red == 4) {
        return true;
    } else if (blue == 4) {
        return true;
    }

    return false;
}


int get_largest_piece_size(int n)
{
    int pieces[] = {BLUE_XLARGE, RED_XLARGE,
                    BLUE_LARGE, RED_LARGE,
                    BLUE_MEDIUM, RED_MEDIUM,
                    BLUE_SMALL, RED_SMALL};

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

// blue is maximizer, red is minimizer
// the sign of the return value determines which is closer to winning
// the value determines how close to winning

// if the returned number is +ve then blue is closer to winning
// if the returned number is -ve then red is closer to winning
// the higher the positive number the closer is blue to winning
// the lower the negative number the closer is red to winning

//hueristics:
//1- number of red/blue pieces in each row/column/diagonal
//2- size of each piece in each row/column/diagonal


unordered_map<unsigned long long, int> calculated_states;

int static_evaluation(State curState)
{
    unsigned long long current_hash = computeHash(curState.board,curState.turn);
    if(calculated_states.find(current_hash)!=calculated_states.end())
    {
        return calculated_states[current_hash];
    }

    // scores for each row, column, diagonal.
    vector<int> row(4, 0);
    vector<int> column(4, 0);
    int main_diagonal = 0;
    int other_diagonal = 0;

    int blue_won = 0;
    int red_won = 0;

    int blue_close = 0;
    int red_close = 0;

    

    // calculate the score of each row.
    for (int i = 0; i < 4; i++)
    {
        int blue = 0;
        int red = 0;

        //counters for blue and red without considering size
        int blue_count=0,red_count=0;

        for (int j = 0; j < 4; j++)
        {
            // if the piece is red and not an empty tile.
            if (get_largest_piece(curState.board[i][j]) > ALL_BLUE and curState.board[i][j] != EMPTY_TILE){
                red-=5; // its a red piece
                red_count--;
                red-=get_largest_piece_size(curState.board[i][j])*2; // also add its size
            }

            // if the piece is red blue and not an empty tile.
            if (get_largest_piece(curState.board[i][j]) < RED_SMALL and curState.board[i][j] != EMPTY_TILE){
                blue+=5; // its a blue piece
                blue_count++;
                blue+=get_largest_piece_size(curState.board[i][j])*2; // also add its size
            }
        }

        row[i] = blue + red;
        if(red_count == -3 && blue_count == 1)red_close += 10;
        if(blue_count == 3 && red_count == -1)blue_close += -10;
        if(red_count == -4)red_won = -1000;
        if(blue_count == 4)blue_won = 1000;

    }

    // columns
    for (int i = 0; i < 4; i++)
    {
        int blue = 0;
        int red = 0;
        int blue_count=0,red_count=0;
        for (int j = 0; j < 4; j++)
        {

            if (get_largest_piece(curState.board[j][i]) > ALL_BLUE and curState.board[j][i] != EMPTY_TILE){
                red-=5; // its a red piece
                red_count--;
                red-=get_largest_piece_size(curState.board[j][i])*2; // also add its size
            }

            if (get_largest_piece(curState.board[j][i]) < RED_SMALL and curState.board[j][i] != EMPTY_TILE){
                blue+=5; // its a blue piece
                blue_count++;
                blue+=get_largest_piece_size(curState.board[j][i])*2; // also add its size
            }
        }

        column[i] = blue + red;
        if(red_count == -3 && blue_count == 1)red_close += 10;
        if(blue_count == 3 && red_count == -1)blue_close += -10;
        if(red_count == -4)red_won = -1000;
        if(blue_count == 4)blue_won = 1000;
    }


    int blue = 0;
    int red = 0;
    int blue_count=0,red_count=0;
    // main diagonal
    for (int i = 0; i < 4; i++)
    {
        if (get_largest_piece(curState.board[i][i]) > 15 and curState.board[i][i] != 0){
            red-=5; // its a red piece
            red_count--;
            red-=get_largest_piece_size(curState.board[i][i])*2; // also add its size

        }

        if (get_largest_piece(curState.board[i][i]) < 16 and curState.board[i][i] != 0){
            blue+=5; // its a blue piece
            blue_count++;
            blue+=get_largest_piece_size(curState.board[i][i])*2; // also add its size
        }

    }


    main_diagonal = blue + red;
    if(red_count == -3 && blue_count == 1)red_close += 10;
    if(blue_count == 3 && red_count == -1)blue_close += -10;
    if(red_count == -4)red_won = -1000;
    if(blue_count == 4)blue_won = 1000;

    blue = 0;
    red = 0;
    blue_count = 0;
    red_count = 0;

    // other diagonal
    for (int i = 0; i < 4; i++)
    {
        if (get_largest_piece(curState.board[i][3 - i]) > ALL_BLUE and curState.board[i][3 - i] != EMPTY_TILE){
            red-=5; // its a red piece
            red_count--;
            red -= get_largest_piece_size(curState.board[i][3 - i])*2; // also add its size
        }

        if (get_largest_piece(curState.board[i][3 - i]) < RED_SMALL and curState.board[i][3 - i] != EMPTY_TILE){
            blue+=5; // its a blue piece
            blue_count++;
            blue += get_largest_piece_size(curState.board[i][3 - i])*2; // also add its size
        }

    }
    other_diagonal = blue + red;
    if(red_count == -3 && blue_count == 1)red_close += 10;
    if(blue_count == 3 && red_count == -1)blue_close += -10;
    if(red_count == -4)red_won = -1000;
    if(blue_count == 4)blue_won = 1000;

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
    int sum_inv1 = curState.inventory[0][0] + curState.inventory[0][1] + curState.inventory[0][2]; 
    int sum_inv2 = curState.inventory[1][0] + curState.inventory[1][1] + curState.inventory[1][2];

    int result =10*(maxx + minn) + 3*(red_close + blue_close) + red_won + blue_won;

    calculated_states[current_hash] = result;

    return  result;
}

bool customSort( State a,  State b) {
            
            return a.static_evl< b.static_evl;
        
        }

//
vector<State> generate_possible_states(State curState, bool sorting)
{
    vector<pair<int, State>> evaluated_states;

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

            if (((largest_piece > ALL_BLUE)) ^ (curState.turn))
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
                    newState.static_evl=static_evaluation(newState);

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
                newState.static_evl=static_evaluation(newState);

                possible_outcome_states.push_back(newState);
            }
        }
    }

    if(sorting)
        sort(possible_outcome_states.begin(), possible_outcome_states.end(),customSort);

    return possible_outcome_states;
}







State minMax_alpha_beta (State postion ,int depth,int alpha , int beta, bool buring, bool mutation)
{ 
    int evl;
    State temp;
    vector<State> childs_States =generate_possible_states(postion, buring);

    if(depth==0) return postion;
    if(postion.turn == 0)//maximizer
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
  
            State minest_state =minMax_alpha_beta(childs_States[i], depth-1,alpha,beta, buring, mutation);
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


    int depth = atoi(argv[arg_index]);
    // itr deepening
    State best_state;
    if(initial_state.turn==0) // max
    best_state.static_evl = INT32_MIN;
    else best_state.static_evl = INT32_MAX;


    for(int i = depth; i<=depth; i++)
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

