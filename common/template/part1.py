'''

'''



import re
from common.common import arg_parse, timer


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()

    lines = data.strip().split('\n')
    
    col1 = sorted(int(line.split()[0]) for line in lines)
    col2 = sorted(int(line.split()[1]) for line in lines)
    
    res = [abs(n1 - n2) for n1, n2 in zip(col1, col2)]
    
    total = sum(res)
    

    #if 'input1.txt' in file_path: assert total == 11
    #if 'input2.txt' in file_path: assert total == 2769675


    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

