'''
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''


from common.common import arg_parse, timer


def find_middle_letter(word):
    return word if len(word) <= 2 else find_middle_letter(word[1:-1])

def remove_middle_letter(word):
    length = len(word)
    if length % 2 == 0:
        return word
    middle_index = length // 2
    return word[:middle_index] + word[middle_index + 1:]


@timer
def find_diagonals(lines, word='MAS'):
    rows, cols, count = len(lines), len(lines[0]), 0
    letter_set, middle_letter = set(remove_middle_letter(word)), find_middle_letter(word)
    buffer = 1
    
    for r in range(buffer, rows - buffer):
        for c in range(1, cols - buffer):
            if lines[r][c] == middle_letter:
                top_left = lines[r - buffer][c - buffer]
                bottom_right = lines[r + buffer][c + buffer]
                top_right = lines[r - buffer][c + buffer]
                bottom_left = lines[r + buffer][c - buffer]

                # Top-left to bottom-right and top-right to bottom-left
                if {top_left, bottom_right} == letter_set and {top_right, bottom_left} == letter_set:
                    count += 1
    return count

@timer
def find_diagonals2(lines, word='MAS'):
    rows, cols = len(lines), len(lines[0])
    letter_set, middle_letter = set(remove_middle_letter(word)), word[len(word) // 2]
    count, buffer = 0, 1
    
    diagonal_offsets = [(-buffer, -buffer), (buffer, buffer)]  # Top-left to bottom-right
    anti_diagonal_offsets = [(-buffer, buffer), (buffer, -buffer)]  # Top-right to bottom-left

    for r in range(buffer, rows - buffer):
        for c in range(buffer, cols - buffer):
            if lines[r][c] == middle_letter:
                # Why do I hate myself?
                diagonal = [lines[r + offset[0]][c + offset[1]] for offset in diagonal_offsets]
                anti_diagonal = [lines[r + offset[0]][c + offset[1]] for offset in anti_diagonal_offsets]

                if {diagonal[0], diagonal[1]} == letter_set and {anti_diagonal[0], anti_diagonal[1]} == letter_set:
                    count += 1
    return count


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()
    lines = data.strip().split('\n')
    
    total1 = find_diagonals(lines)
    total2 = find_diagonals2(lines)
    
    assert total1 == total2
    
    print(total1)
    
    if 'input3.txt' in file_path: assert total1 == 9
    if 'input2.txt' in file_path: assert total1 == 1831

    return total1
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input3.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

