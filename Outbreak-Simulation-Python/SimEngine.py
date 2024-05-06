# Author: Rutvik Tondwalkar
# Date: 10/24/2023
# Description: SimEngine.py asks the user for a configuration file
# and simulates the outbreak and displays the region data.

# Import functions from SimLibrary
from SimLibrary import read_configuration_file, simulate_outbreak, plot


def main():
    """ Call the function read_configuration_file()
     read_configuration_file() asks the user for input file name
     simulate_outbreak() simulates the outbreak and displays the region data
     """

    # define empty lists
    region = []
    s = []
    i = []
    r = []

    threshold, infectious_period, region = read_configuration_file(region)

    # Initialise the SIR List
    s = [sum(row.count('s') for row in region)]
    i = [sum(row.count('i') for row in region)]
    r = [sum(row.count('r') for row in region)]

    # Simulate the outbreak
    updated_region, susceptible, infectious, recovered, days = simulate_outbreak(region, threshold, infectious_period, s, i, r)

    # Output outbreak statistics
    print(f"Outbreak Duration: {days} days")
    max_infectious = max(infectious)
    max_day = infectious.index(max_infectious)
    print(f"Peak Day: Day {max_day}")
    print(f"Peak Infectious Count: {max_infectious} people")

    # Plot Daily S I R counts
    plot(susceptible, infectious, recovered)


# Call main function
main()
