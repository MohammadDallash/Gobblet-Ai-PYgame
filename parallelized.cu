#include <cstring>
#include <ctime> 
#include <iostream>
#include <string>
#include <algorithm>
#include <cstdint>
#include <climits>
#include <random>

const int BOARD_SIZE = 4;
const int NUMBER_OF_PLAYERS = 2;
const int INVENTORY_SIZE = 3;
#define db(x) printf("%s\n", x)

using namespace std;

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
    int lastMove[2][3];
    int static_evl;
};



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

#define fori(size) for (int i = 0; i < (size); i++)
#define forj(size) for (int j = 0; j < (size); j++)
#define fork(size) for (int k = 0; k < (size); k++)
const int INVENTORY_MOVE = 0;
const int BOARD_MOVE = 1;



__device__ int get_largest_piece(int n);
__device__ bool checkWins(State s);
__device__ int get_largest_piece_size(int n);
__device__ __host__ void debug_state(State state);
__device__ int static_evaluation(State curState);
__device__ bool customSort( State a,  State b);
__device__ void generate_possible_states(State curState, bool sorting,  int &n_child, State* &a);



using namespace std;

__device__ int get_largest_piece(int n)
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


__device__ bool checkWins(State s) 
{
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



__device__ int get_largest_piece_size(int n)
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
__device__ __host__ void debug_state(State state) {
    printf("Turn: %d\n\n", state.turn);

    printf("Board:\n");
    fori(BOARD_SIZE) {
        forj(BOARD_SIZE) {
            printf("%d ", state.board[i][j]);
        }
        printf("\n");
    }

    printf("\nInventory:\n");
    fori(NUMBER_OF_PLAYERS) {
        forj(INVENTORY_SIZE) {
            printf("%d ", state.inventory[i][j]);
        }
        printf("\n");
    }
    printf("\n");

    printf("Last Move:\n\n");
    fori(2) {
        forj(INVENTORY_SIZE) {
            printf("%d ", state.lastMove[i][j]);
        }
        printf("\n");
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


// unordered_map<unsigned long long, int> calculated_states;

__device__ int static_evaluation(State curState)
{
    // unsigned long long current_hash = computeHash(curState.board,curState.turn);
    // if(calculated_states.find(current_hash)!=calculated_states.end())
    // {
    //     return calculated_states[current_hash];
    // }

    // scores for each row, column, diagonal.
    int row[] = {0,0,0,0};
    int column[] = {0,0,0,0};
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


    int result =10*(maxx + minn) + 3*(red_close + blue_close) + red_won + blue_won;

    // calculated_states[current_hash] = result;

    return  result;
}

__device__ bool customSort( State a,  State b)
{            
    return a.static_evl< b.static_evl;
        
}




__device__ int getFlattenedIndexInDst(int i, int j, int k)
{
    const int  d2 = 16, d3 = 3;

    return i * (d2 * d3) + j * d3 + k;
}


__device__ void generate_possible_states(State curState, bool sorting,  int &n_child, State* &a)
{

   

    if (checkWins(curState))
    {

        cudaMalloc((void**)&a, sizeof(State) * 1);
        cudaDeviceSynchronize();

        
        n_child ++;
        a[0] = curState;

        
        return;
    }


    
    const int d1 = 5, d2 = 16, d3 = 3;


    //  locations where each size exists (in the board and the inventory)

    int *possible_destination;
    cudaMalloc((void**)&possible_destination, sizeof(int) * d1 * d2 * d3);
    cudaDeviceSynchronize();



    int *p;
    cudaMalloc((void**)&p, sizeof(int) * 5);

    cudaDeviceSynchronize();

    p[0]=0;
    p[1]=0;
    p[2]=0;
    p[3]=0;
    p[4]=0;




    
    cudaMalloc((void**)&a, sizeof(State) * 120);
    cudaDeviceSynchronize();


    
    // add each location to its corresponding size

    fori(BOARD_SIZE)
    {
        forj(BOARD_SIZE)
        {
             
            int size = get_largest_piece_size(curState.board[i][j]);


            int idx = getFlattenedIndexInDst(size, p[size], 0);
            p[size]++;
            cudaDeviceSynchronize();



            possible_destination[idx] = BOARD_MOVE;
            possible_destination[idx+1] = i;
            possible_destination[idx+2] = j;
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
                for (int d = 0; d < p[s]; d++)
                {
                    int *dest = possible_destination + getFlattenedIndexInDst(s,d,0);



                    State newState = curState;


                    newState.board[dest[1]][dest[2]] |= largest_piece;
                    newState.board[i][j] &= ~(largest_piece);



                    newState.lastMove[0][0] = BOARD_MOVE;
                    newState.lastMove[0][1] = i;
                    newState.lastMove[0][2]  = j;



                    newState.lastMove[1][0] = dest[0];
                    newState.lastMove[1][1] = dest[1];
                    newState.lastMove[1][2] = dest[2];




                    newState.turn = curState.turn ^ 1;
                    newState.static_evl=static_evaluation(newState);



                    a[n_child++] = newState;
                }
            }
        }
    }

  


    fori(INVENTORY_SIZE)
    {
        int curPiece = curState.inventory[curState.turn][i];

        int size = get_largest_piece_size(curPiece);

        int largest_piece = get_largest_piece(curPiece);
        
        


        for (int s = 0; s < size; s++)
        {
            for (int d = 0; d < p[s]; d++)
            {
                int *dest = possible_destination + getFlattenedIndexInDst(s,d,0);



                State newState = curState;


                newState.board[dest[1]][dest[2]] |= largest_piece;
                newState.inventory[curState.turn][i] &= ~(largest_piece);


                newState.lastMove[0][0] = INVENTORY_MOVE;
                newState.lastMove[0][1] = curState.turn;
                newState.lastMove[0][2]  = i;

                
                
                newState.lastMove[1][0] = dest[0];
                newState.lastMove[1][1] = dest[1];
                newState.lastMove[1][2] = dest[2];




                newState.turn = curState.turn ^ 1;
                newState.static_evl=static_evaluation(newState);



                
                a[n_child++] = newState;


            }
        }
    }


    cudaFree(p);
    cudaDeviceSynchronize();

    cudaFree(possible_destination);
    cudaDeviceSynchronize();


    if(sorting)
    {
        // sort(a, a + n_child, customSort);;
        ;
    }
}




__device__ State minMax_alpha_beta (State postion ,int depth,int alpha , int beta, bool buring, bool mutation, int difficulty)
{ 
    
    int evl;
    State temp;
    int n_child = 0;
    State * a;
    if(depth==0) return postion;

      

    generate_possible_states(postion, buring ,n_child ,a);


    printf(""); // magiccc

    cudaDeviceSynchronize();










    if(postion.turn == 0)//maximizer
    {

        int largest_Eval=INT32_MIN;
        // reverse(a,a + n_child );
        for(int i=0;i<n_child;i++)
        {  
            State largest_state =minMax_alpha_beta (a[i], depth-1,alpha,beta, buring, mutation, difficulty);
            cudaDeviceSynchronize();


            evl=largest_state.static_evl;
            alpha=max(evl,alpha);
            if(evl>largest_Eval or (evl== largest_Eval and mutation /*and rand()%3 == 1*/))
            {
                temp = a[i];
                largest_Eval = evl;
            }

            if(alpha>= beta and buring)break;
        }
    }
    else // minimizer
    {

        
        int minest_Eval=INT32_MAX;
        for(int i=0;i<n_child;i++)
        {
            State minest_state =minMax_alpha_beta(a[i], depth-1,alpha,beta, buring, mutation, difficulty);
            cudaDeviceSynchronize();


            evl=minest_state.static_evl;
            beta=min(beta,evl);

            if(evl<minest_Eval or (evl== minest_Eval and mutation /*and rand()%3 == 1*/))
            {
                temp = a[i];
                minest_Eval = evl;
            }

            if(alpha>= beta and buring)  break;
            
        }
    }

    cudaFree(a);
    cudaDeviceSynchronize();


    return temp;
}

#pragma no_auto_parallel
__device__ State tt(State s)
{
    auto o = minMax_alpha_beta(s, 2, INT32_MIN, INT32_MAX, true, true,1 );
    cudaDeviceSynchronize();

    return o;
}


__global__ void kernel(State s, State* o)
{
    State an = tt(s);
    *o = an;
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


    int  difficulty = atoi(argv[arg_index]);

    
    
    State *an;

    // Allocate memory for each vector on GPU
    cudaMalloc(&an, sizeof(State));

    kernel<<<1, 1>>>(initial_state, an);
    cudaDeviceSynchronize();

    // Allocate memory for anH on the host
    State *anH = (State*)malloc(sizeof(State));

    cudaMemcpy(anH, an, sizeof(State), cudaMemcpyDeviceToHost);

    // Now you can use anH as needed

    debug_state(*anH);


    // Don't forget to free the allocated memory on the host
    free(anH);

    // Don't forget to free the allocated memory on the device
    cudaFree(an);
    return 0;
}

/*
./a.out 1 0 128 128 128  0 0 0 0  0 0 0 0  0 0 0 0   7 7 7  112 112 112  3
*/