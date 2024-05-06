//Name - Rutvik Tondwalkar
//Date - 03/07/2024
//Description - Driver.cpp

#include "Outbreak.h"
#include <iostream>
using namespace std;


int main(){

    int H,W,T,I;

    Person** data = Parse_config_file(H, W, T, I);
    simulate_outbreak(data, H, W, T, I);
    
    return 0;
}