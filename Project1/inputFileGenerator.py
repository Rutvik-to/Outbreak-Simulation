# Author: Rutvik Tondwalkar
# Date: 10/24/2023
# Description: This python code takes various input parameters from the user and
# outputs a .txt file. This file is an input file for SimEngine.py

import random


def generate_input_file(region_dimension, infected_number, vaccinated_number, threshold,
                        infection_period, file_name):
    """Generates an input.txt file for the simulation.
    :param region_dimension: A list of two integers representing the rows and columns of the region.
    :type region_dimension: list
    :param infected_number: The number of infectious people in the region at the start of the simulation.
    :type infected_number: int
    :param vaccinated_number: The number of vaccinated people in the region at the start of the simulation.
    :type vaccinated_number: int
    :param threshold: The probability of becoming infected if exposed to the disease.
    :type threshold: int
    :param infection_period: The number of days that an infected person is contagious.
    :type infection_period: int
    :param file_name: The name of the input file to generate.
    :type file_name: str
  """
    # open the file in write mode
    with open(file_name, "w") as myFile:
        # Write first line for threshold
        myFile.write(f"Threshold:{threshold}\n")

        # Write second line for infectious period
        myFile.write(f"Infectious Period:{infection_period}\n")

        # Generate an initial region configuration with all 's'.
        region = []
        for i in range(region_dimension[0]):
            region.append(["s" for i in range(region_dimension[1])])

        # Using random, generate a random cell and replace it with "i".
        for k in range(infected_number):
            i = random.randint(0, region_dimension[0] - 1)
            j = random.randint(0, region_dimension[1] - 1)
            region[i][j] = "i"

        # Using random, generate a random cell number and replace it with "v".
        for k in range(vaccinated_number):
            i = random.randint(0, region_dimension[0] - 1)
            j = random.randint(0, region_dimension[1] - 1)
            region[i][j] = "v"

        # Write the initial configuration of the region to the input file.
        for row in region:
            myFile.write(",".join([str(x) for x in row]))
            myFile.write("\n")


# Prompt the user for the dimensions of the region.
rows = int(input("Please enter the number of rows: "))
columns = int(input("Please enter the number of columns: "))
region_dim = [rows, columns]
population = region_dim[0]*region_dim[1]

# Prompt the user for the remaining parameters.
print(f"The total population of the specified region is {population}")
num_infectious = int(input("Please enter the number of infected people: "))
num_vaccinated = int(input("Please enter the number of vaccinated people: "))
infection_threshold = int(input("Please enter the threshold for infection: "))
infectious_period = int(input("Please enter the infectious period: "))
input_file_name = input("Please specify the name of the input file with .txt extension: ")

# Call the generate_input_file function and pass the input parameters to generate the required input file
generate_input_file(region_dim, num_infectious, num_vaccinated, infection_threshold,
                    infectious_period, input_file_name)

print("Yayy! The input file has been generated successfully!")
