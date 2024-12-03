'''

'''



import re
from common.common import arg_parse, timer


def main(file_path):
    data = open(file_path, 'r', encoding='utf-8').read()

    lines = data.strip().split('\n')

    

    #if 'input1.txt' in file_path: assert total == 11
    #if 'input2.txt' in file_path: assert total == 2769675


    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)

