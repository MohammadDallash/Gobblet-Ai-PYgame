#include <iostream>
#include <vector>
using namespace std;

int main(){
    vector<vector<int>> vec(4, vector<int> (4, 0));

    for(int i = 0; i<4; i++){
        for(int j = 0; j<4; j++){
            cin>>vec[i][j];
        }
    }
    

    cout<<vec[0][0]+vec[1][1]+vec[2][2]+vec[3][3];
    
}

