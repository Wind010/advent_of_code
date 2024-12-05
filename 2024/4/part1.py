'''
https://adventofcode.com/2024/day/4
'''


from common.common import arg_parse, timer, assertions


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


def find_word_count_ropatel(matrix):
    wordCount, limit = 0, len(matrix)

    # Horizontal Right to Left
    for y in range(limit):
        for x in range(limit):
            
            # backward case
            if (matrix[y][x]=="S" and (x+3) < limit):
                test = matrix[y][x] + matrix[y][x+1] + matrix[y][x+2] + matrix[y][x+3]
                if (test=="SAMX"):
                    wordCount+=1

            # forward case
            if (matrix[y][x]=="X" and (x+3)< limit):
                test = matrix[y][x] + matrix[y][x+1] + matrix[y][x+2] + matrix[y][x+3]
                if (test=="XMAS"):
                    wordCount+=1


    # Vertical Up Down
    for x in range(limit):
        for y in range(limit):

            # backward case
            if (matrix[y][x]=="S" and (y+3) < limit):
                test = matrix[y][x] + matrix[y+1][x] + matrix[y+2][x] + matrix[y+3][x]
                if (test=="SAMX"):
                    wordCount+=1

            # forward case
            if (matrix[y][x]=="X" and (y+3)< limit):
                test = matrix[y][x] + matrix[y+1][x] + matrix[y+2][x] + matrix[y+3][x]
                if (test=="XMAS"):
                    wordCount+=1


    # Right Diagonal            
    for y in range(limit):
        for x in range(limit):
            
            # backward case
            if (matrix[y][x]=="S" and ((y+3)< limit and (x+3) < limit)):
                test = matrix[y][x] + matrix[y+1][x+1] + matrix[y+2][x+2] + matrix[y+3][x+3]
                if (test=="SAMX"):
                    wordCount+=1

            # forward case
            if (matrix[y][x]=="X" and ((y+3)<limit and (x+3) < limit)):
                test = matrix[y][x] + matrix[y+1][x+1] + matrix[y+2][x+2] + matrix[y+3][x+3]
                if (test=="XMAS"):
                    wordCount+=1

    # Left Diagonal            
    for y in range(limit):
        for x in range(limit-1,0,-1):
            
            # backward case
            if (matrix[y][x]=="S" and ((y+3)<limit) and (x-3) >= 0):
                test = matrix[y][x] + matrix[y+1][x-1] + matrix[y+2][x-2] + matrix[y+3][x-3]
                if (test=="SAMX"):
                    wordCount+=1

            # forward case
            if (matrix[y][x]=="X" and ((y+3)<limit) and (x-3) >= 0):
                test = matrix[y][x] + matrix[y+1][x-1] + matrix[y+2][x-2] + matrix[y+3][x-3]
                if (test=="XMAS"):
                    wordCount+=1

    return wordCount


def main(args, data):
    lines = data.strip().split('\n')

    total = find_word_count(lines)
    print(total)
    
    total2 = find_word_count_ropatel(lines)
    
    assert total == total2
    
    assertions(args, total, 18, 2336)

    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
