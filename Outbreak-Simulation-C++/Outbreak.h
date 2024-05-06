//Name - Rutvik Tondwalkar
//Date - 03/07/2024
//Description - Outbreak.h

#ifndef OUTBREAK_H
#define OUTBREAK_H

// Struct to store person's health state and days infected.
struct Person
{
    char State;
    int Period = 0;
    int infected;
};

// Function declarations
Person** Parse_config_file(int &H, int &W, int &T, int &I);
void simulate_outbreak(Person** region, int height, int width, int threshold, int infectious_period);
void print_region(Person** region , int height, int width);

#endif