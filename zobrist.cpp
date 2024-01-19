#include <ctime>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdint>
#include <unordered_set>
#include <climits>
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

unsigned long long computeHash(int board[][4])
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
    return h;
}



int main()
{
    fill_table();
    cout << computeHash(board) << endl;
}
