'''
--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
'''

import argparse
from functools import reduce
import os

import re
from operator import mul
from part1 import RED, GREEN, BLUE


#RED, BLUE, GREEN = 'red', 'blue', 'green'

def get_fewest_cubes_of_each_color(line):
    _, sets_info = line.split(':')

    cubes = {
        RED: 0,
        GREEN: 0,
        BLUE: 0
    }

    for set_info in sets_info.split(';'):
        for cube in set_info.split(','):
            count_str, color = cube.split()
            count = int(count_str.strip())
            
            if count > cubes[color]:
                cubes[color] = count

    return cubes
  
def get_fewest_cubes_of_each_color_regex(line):
    cubes = {
        RED: 0,
        GREEN: 0,
        BLUE: 0
    }
    sets_info = re.findall(r'(\d+) (\w+)', line.split(':')[1])
    
    for count, color in sets_info:
        count = int(count.strip())
        if count > cubes.get(color.strip(), 0):
            cubes[color] = count

    return cubes
		
  
def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.split('\n')
    
    cubes = [get_fewest_cubes_of_each_color_regex(line) for line in lines]
    powers = [reduce(mul, cube.values()) for cube in cubes]
    total_powers = sum(powers)
        
    print(cubes, powers, total_powers)
    
    if 'input1.txt' in file_path: assert total_powers == 2286
    if 'input2.txt' in file_path: assert total_powers == 60948

    return total_powers
    

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_file_path = os.path.join(current_dir, 'input2.txt')
    
    parser = argparse.ArgumentParser(description="🖖")
    parser.add_argument("file_path", type=str, nargs='?', 
        default=default_file_path, help="The path to the file containing the input data.")
    args = parser.parse_args()
    
    main(args.file_path)
		