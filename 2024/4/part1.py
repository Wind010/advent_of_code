'''
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

To begin, get your puzzle input.
'''


from common.common import arg_parse, timer


def find_word_in_diagonals(lines, word):
    rows, cols, count = len(lines), len(lines[0]), 0
    for r in range(rows):
        for c in range(cols):
            #count += traverse_direction(row, col, lines, -1, -1, word)   # Upper left
            #count += traverse_direction(row, col, lines, -1, 1, word)    # Upper right
            count += traverse_direction(r, c, lines, 1, -1, word)    # Lower left
            count += traverse_direction(r, c, lines, 1, 1, word)     # Lower right
            
            # or this if four diagonal directions but it's only three from observation.
            # count += sum([traverse_direction(row, col, lines, dir_x, dir_y, word)
            #           for dir_x, dir_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]])
    return count


def traverse_direction(row, col, lines, row_dir, col_dir, word):
    rows, cols = len(lines), len(lines[0])
    for i, letter in enumerate(word):
        r, c = row + i * row_dir, col + i * col_dir
        if r < 0 or r >= rows or c < 0 or c >= cols or lines[r][c] != letter:
            return 0
    return 1


@timer
def find_word_count(lines, word='XMAS'):
    #count = sum(1 for line in lines if word in line or word[::-1] in line) # Doesn't count total occurance.
    count = sum(line.count(word) + line.count(word[::-1]) for line in lines)

    transposed_lines = [''.join(line[i] if i < len(line.strip()) else ' ' for line in lines) 
                        for i in range(len(lines))]
    #print(transposed_lines)
    count += sum(line.count(word) + line.count(word[::-1]) for line in transposed_lines)
    
    count += find_word_in_diagonals(lines, word)
    count += find_word_in_diagonals(lines, word[::-1])

    return count


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.strip().split('\n')

    total = find_word_count(lines)
    print(total)
    
    if 'input1.txt' in file_path: assert total == 18
    if 'input2.txt' in file_path: assert total == 2336

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

