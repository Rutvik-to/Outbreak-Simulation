# Author: Rutvik Tondwalkar
# Date: 10/24/2023
# Description: This python code contains all the necessary functions
# for SimEngine.py

import matplotlib.pyplot as plt


def print_region(region, day):
    """
    print_region takes a list named region and
    an int named day and displays it in an easy-to-read format
    :param region: Region (2D list of ['s', 'i', 'r', 'v'] data)
    :type region: List
    :param day: Day of simulation
    :type day: int
    :return: Void.
    """
    print(f"Day {day}:")
    for row in region:
        print(' '.join(row))
    print()


def read_configuration_file(region):
    """
    Prompts the user for input file name. Reads the input file and stores the data.
    Throws appropriate errors when the config file is not as expected.
    :param region: Region (2D list of ['s', 'i', 'r', 'v'] data)
    :type region: List
    :return: Threshold, Infectious_period, region.
    """
    try:
        # Prompt the user for the configuration file
        file_name = input("Enter the name of the configuration file: ")

        # Open the file then read it and store it
        file = open(file_name, "r")
        lines = file.readlines()

        # Convert first line into a list and strip white spaces
        th = list(lines[0].strip())

        # Store the last element in threshold variable
        threshold = int(th[-1])

        # Convert second line into a list and strip white spaces.
        ip = list(lines[1].strip())

        # Raise an error if there is a problem in the second line
        # Check the first element of the ip list. if it is region data, raise an error.
        if ip[0] == 's':
            raise IOError("ERROR: There's something wrong with the input file!")

        # If there is no error in the file, save the last element of the list ip as infectious_period variable.
        ip = int(ip[-1])
        infectious_period = ip

        # store the remaining lines i.e. from line 2 till the end as a 2D list
        res = [str(line.strip()) for line in lines[2:]]

        # go through all the elements of res list and remove all commas. store the new data in region list
        for row in res:
            row = row.split(",")
            region.append(row)

        # Check if all the elements in the region_data are either "s","i","r" or "v"
        # if not then raise an error
        valid_health_states = ['s', 'i', 'r', 'v']
        for row in region:
            for state in row:
                if state not in valid_health_states:
                    raise ValueError(f"ERROR: {state} is not a valid state!")
        # Print Region Data at day 0
        print_region(region, day=0)

        return threshold, infectious_period, region

    # Raise an error if input file is not found and ask user to input the filename again
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")
        return read_configuration_file(region)
    # Raise an error if any invalid state is detected and exit with exit code -1
    except ValueError as e:
        print(e)
        exit(-1)
    # Raise an error if the configuration file is not as expected and exit with exit code -2
    except IOError as e:
        print(e)
        exit(-2)


def simulate_outbreak(region, threshold, infectious_period, susceptible_count, infectious_count, recovered_count):
    """
    Simulates the outbreak
    :param region: Region (2D list of ['s', 'i', 'r', 'v'] data)
    :type region: List
    :param threshold: Threshold of nearby infected people to infect new susceptible people
    :type threshold: int
    :param infectious_period: Days after which infected are recovered
    :type infectious_period: int
    :param susceptible_count: number of susceptible people
    :type susceptible_count: List
    :param infectious_count: number of infected people
    :type infectious_count: List
    :param recovered_count: number of recovered people
    :type recovered_count: List
    :return: region, susceptible_count, infectious_count, recovered_count, day.
    """
    day = 0

    # Generate a 2D list to keep a track of infected people and their days
    infected_days = []

    for row in region:
        infected_days.append([0 for k in row])
    for i in range(len(region)):
        for j in range(len(region[i])):
            test = region[i][j]
            if test == "i":
                infected_days[i][j] = 1

    # Simulation of the outbreak
    while infectious_count[-1] > 0:
        new_day = []
        for i in range(len(region)):
            new_row = []
            for j in range(len(region[i])):
                cell = region[i][j]
                if cell == 'v':  # Vaccinated cells do not change
                    new_row.append('v')
                elif cell == 's':
                    # Count number of infected neighbours and change s to i if it exceeds the threshold
                    num_infectious_neighbors = count_infectious_neighbors(region, i, j)
                    if num_infectious_neighbors >= threshold:
                        new_row.append('i')
                        # update the infected days count
                        infected_days[i][j] += 1
                    else:
                        new_row.append('s')
                elif cell == 'i':
                    # if the cell is infected and the number of days it is infected exceeds infectious_period
                    # Then change it to recovered else increment the infected_days cell.
                    if infected_days[i][j] >= infectious_period:
                        new_row.append('r')
                    else:
                        new_row.append('i')
                        infected_days[i][j] += 1  # Increment days infected
                elif cell == 'r':
                    # If the cell is recovered, keep it recovered
                    new_row.append('r')
            new_day.append(new_row)

        # Update the region list and the day
        region = new_day
        day += 1

        # Print the state of the region for the current day
        print_region(region, day)

        # update the total number of S I R list daily
        susceptible_count.append(sum(row.count('s') for row in region))
        infectious_count.append(sum(row.count('i') for row in region))
        recovered_count.append(sum(row.count('r') for row in region))

    return region, susceptible_count, infectious_count, recovered_count, day


def count_infectious_neighbors(region, i, j):
    """
    Counts the number of infectious neighbours for every cell
    :param region: Region (2D list of ['s', 'i', 'r', 'v'] data)
    :type region: List
    :param i: row index
    :type i: int
    :param j: column index
    :type j: int
    :return: infectious_neighbours
    """
    rows, cols = len(region), len(region[0])
    infectious_neighbors = 0
    # checks for infectious cells one row above and one row below
    # checks for infectious cells one column left and one column right
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if 0 <= x < rows and 0 <= y < cols and region[x][y] == 'i':
                infectious_neighbors += 1
    return infectious_neighbors


def plot(susceptible, infectious, recovered):
    """
    Plots the S I R on a plot using matplotlib
    :param susceptible: Susceptible data for each day
    :type susceptible: List
    :param infectious: Infectious data for each day
    :type infectious: List
    :param recovered: Recovered data for each day
    :type recovered: List
    :return: Void
    """
    x = ["S", "I", "R"]
    y_axis = [susceptible, infectious, recovered]
    x_axis = len(susceptible)
    x_axis = list(range(0, x_axis))

    # plot the S I R w.r.t Days
    for i in range(len(x)):
        plt.plot(x_axis, y_axis[i], label=x[i])

    # Display Title, labels and legend
    plt.title("SIR State Counts")
    plt.xlabel("Days")
    plt.ylabel("Counts")
    plt.legend(x)

    # display the plot
    plt.show()
