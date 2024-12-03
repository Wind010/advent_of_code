'''
As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200
...now instead means this:

Time:      71530
Distance:  940200
Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?'''

import re
import math
from functools import reduce
from common.common import arg_parse, timer


def parse_lines(input):
    return int("".join(re.findall(r'\d+', input[0]))), int("".join(re.findall(r'\d+', input[1])))

@timer
def simulate_race_bounds(time, distance):
    '''
    Find lower and upper bound to determine the winning range
    '''
    lower_bound, upper_bound = 0, 0
    for held in range(time + 1):
        travelled = held * (time - held)
        if travelled > distance:
            lower_bound = held
            break
    for held in range(time, 0, -1):
        travelled = held * (time - held)
        if travelled > distance:
            upper_bound = time - held
            break
    
    return (time + 1) - lower_bound - upper_bound

@timer
def simulate_race_acceleration(time, distance):
    '''
    Use kinematic equations of motion, specifically the quadrative equation of a*t^2 + v*t + d = 0.
    Solve for acceleration with velocity = 0 and d is the distance traveled.
    d = 1/2a*t^2 
    Then re-arrange for to solve for a:
    a = 2d/t^2
    '''
    # The time**2 - 4*distance is the discriminant of the quadratic formula.
    exact_acceleration = (time - math.sqrt((time**2 - 4*distance))) / 2 
    min_acceleration = int(exact_acceleration + 1) # Round up
    return time - 2*min_acceleration + 1 

@timer
def simulate_race_roots(time, distance):
    '''
    t = T - B
    Where:
        t is travel time
        T is total race time,
        B button pressed time

    D = t * B
    Where
        D is the traveled distance
        t is the travel time
        B is the button pressed time
        
    Substituting 1 in 2 and simplifying we get:
    D = (T - B) * B 
    D = T*B - B^2      
    B^2 - T*B + D = 0 
    
    Now we can use the quadratic formula to solve for B, and setting D to the record distance + 1
    B1 = (T + SQRT(T*T - 4 * D))/2
    B2 = (T - SQRT(T*T - 4 * D))/2
    
    Number of Races that set a new record B1 - B2 which is the number of integer solutions between the two record point solutions
    Shown in 6.ipynb
    '''
    # Find the differences between the two roots.
    b1 = math.floor((time + math.sqrt(pow(time, 2) - 4 * distance))/2)
    b2 = math.ceil((time - math.sqrt(pow(time, 2) - 4 * distance))/2)

    return b1 - b2 + 1


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    time, distance = parse_lines(data.split("\n"))
     
    possible_wins = simulate_race_bounds(time, distance)
    print(possible_wins)
    
    if 'input1.txt' in file_path: assert possible_wins == 71503 
    if 'input2.txt' in file_path: assert possible_wins == 34655848

    possible_wins = simulate_race_acceleration(time, distance)
    print(possible_wins)
    
    if 'input1.txt' in file_path: assert possible_wins == 71503 
    if 'input2.txt' in file_path: assert possible_wins == 34655848

    possible_wins = simulate_race_roots(time, distance)
    print(possible_wins)
    
    if 'input1.txt' in file_path: assert possible_wins == 71503 
    if 'input2.txt' in file_path: assert possible_wins == 34655848


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

