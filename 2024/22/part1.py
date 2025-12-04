'''
https://adventofcode.com/2024/day/22
'''



import re
from common.common import arg_parse, assertions, timer

MODULO = 16777216

def next_secret(secret):
    # Step 1: Multiply by 64, mix, prune
    secret = (secret * 64) ^ secret
    secret %= MODULO
    
    # Step 2: Divide by 32, round down, mix, prune
    secret = (secret // 32) ^ secret
    secret %= MODULO
    
    # Step 3: Multiply by 2048, mix, prune
    secret = (secret * 2048) ^ secret
    secret %= MODULO
    
    return secret

def get_2000th_secret(initial_secret):
    secret = initial_secret
    for _ in range(2000):
        secret = next_secret(secret)
    return secret

def sum_of_2000th_secrets(initial_secrets):
    total = 0
    for initial_secret in initial_secrets:
        total += get_2000th_secret(initial_secret)
    return total


def main(args, data):
    lines = data.strip().split('\n')
    initial_secrets = [*map(int, lines)]
    
    result = sum_of_2000th_secrets(initial_secrets)
    
    assertions(args, result, 37327623, 16953639210, 13764677935)
    return result
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

