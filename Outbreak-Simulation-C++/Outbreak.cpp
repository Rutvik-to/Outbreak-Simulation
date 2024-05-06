//Name - Rutvik Tondwalkar
//Date - 03/07/2024
//Description - Outbreak.cpp

#include "Outbreak.h"
#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>


using namespace std;


// Read Config file and parse data
// Input - pass by reference height, width , threshold and infectious period
// Return - double pointer of struct Person
// Description :- Prompts the user for config file name and parse the information provided in the file.
Person** Parse_config_file(int &H, int &W, int &T, int &I){
    
    // Initialise Variables
    string userInput,Width,Height,Infectious_period,Threshold,Region;
    int D;

    do{
        // Ask the user for .txt filename, keep asking if file not found.
        cout << "Please enter the name of the configuration file: ";
        cin >> userInput;
        ifstream configFile(userInput);
        if(!configFile.is_open()){
            cout << userInput << " does not exists! ";
        }
        else{
            configFile.close();
            break;
        }
    }while(true);

    ifstream configFile(userInput);

    // Parse Config file
    getline(configFile, Height);
    getline(configFile, Width);
    getline(configFile, Threshold);
    getline(configFile, Infectious_period);
    getline(configFile, Region);

    // Parse every line to extract data
    Height = Height.substr(14);
    Width = Width.substr(13);
    Threshold = Threshold.substr(10);
    Infectious_period = Infectious_period.substr(18);
    Region = Region.substr(12);

    // Convert string to int
    H = stoi(Height);
    W = stoi(Width);
    T = stoi(Threshold);
    I = stoi(Infectious_period);

    // create instances of struct in 2D array 
    Person** region = new Person*[H];
    for (int i = 0; i < H; i++) {
        region[i] = new Person[W];
    }
    
    string data;
    ifstream RegionFile(Region);

    // Print Day 0
    cout << "Day: " << D << endl;

    // Store region data in a 2D array
    for(int i = 0; i < H; i++){
        for(int j = 0; j < W-1; j++){
            getline(RegionFile, data, ',');
            region[i][j].State = (char)data[0];
            cout << region[i][j].State << " ";

            if(j == W - 2){
                getline(RegionFile, data);
                region[i][W-1].State = (char)data[0];
                cout << region[i][W-1].State;
            }
        }
        cout << endl;
    }
    cout << endl;

    // Return pointer to 2D Array
    return region;

}

// Print Function 
// Input - 2D Array of struct Person, Region height and width
// Return - void
// Description :- Prints the region
void print_region(Person** region , int height, int width){

    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            cout << region[i][j].State << " ";
        }
        cout << endl;
    }

    cout << endl;
}

// Simulate outbreak
void simulate_outbreak(Person** region, int height, int width, int threshold, int infectious_period){

    // Initilise variables
    int D = 0;
    int index = 0;
    int I_max = 0;
    int D_max = 0;
    float I_cum = 0;

    // Iterate every day, break upon no infected left
    while (true){
        
        int I_count = 0;
        int V_count = 0;
        int S_count = 0;
        int R_count = 0;

        // Count S I R V in the region
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){
                if (region[i][j].State == 'S'){
                    S_count++;
                }
                else if (region[i][j].State == 'I'){
                    I_count++;
                }
                else if (region[i][j].State == 'R'){
                    R_count++;
                }
                else if (region[i][j].State == 'V'){
                    V_count++;
                }
            }   
        }

        // Check which cells needs to be updated for next day
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){

                int neighbours = 0;
            
                if(region[i][j].State == 'S'){
                    
                    // Count infected neighbours
                    for (int a = i - 1; a < i + 2; a++){
                        for (int b = j - 1; b < j + 2; b++){
                            if(a >= 0 && b >= 0 && a < height && b < width && region[a][b].State == 'I'){
                               neighbours++;
                            }
                        }
                    }

                    // Infected next day; Yes or No
                    if( neighbours >= threshold ){
                    region[i][j].infected = 1;
                    }
                }

                // increment infected period by 1
                if (region[i][j].State == 'I'){
                    region[i][j].Period += 1;
                }
            }
        }

        // Region update
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){

                if(region[i][j].infected == 1){
                    region[i][j].State = 'I';
                }

                if(region[i][j].Period >= infectious_period){
                    region[i][j].State = 'R';
                }

                if(region[i][j].State == 'R'){
                    region[i][j].State = 'R';
                }

                if(region[i][j].State == 'V'){
                    region[i][j].State = 'V';
                }
            }
        }
        
        // count cumulative infected for average
        I_cum += I_count;
        
        // calculate max infected
        if (I_count > I_max){
            I_max = I_count;
            D_max = D;
            cout << I_max << endl;
            cout << D_max << endl;
        }

        // Output data and break when everyone is recovered
        if(I_count == 0){
            
            cout << "The outbreak took " << D << " days to end." << endl;
            cout << "The peak infectious count was " << I_max << " people at day "<< D_max << "." << endl;
            cout << "The average number of infectious people per day was "<< setprecision(4) << showpoint << I_cum/D << " people." << endl;
            cout << "The final counts of susceptible, infectious, recovered people was:" << endl;
            cout << "Susceptible: " << S_count << endl;
            cout << "Infectious:  " << I_count << endl;
            cout << "Recovered:   " << R_count << endl;
            cout << "Vaccinated:  " << V_count << endl;
            break;
        }
        
        D++;
        cout << "Day: " << D << endl;
        index++;
        print_region(region, height, width);
    }
}


