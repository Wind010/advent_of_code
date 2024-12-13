import os
import argparse

import time
from functools import wraps

from typing import Callable

# If class, then __init__.py would resolve.

def arg_parse(file: str, input_file: str, main: Callable):
    current_dir = os.path.dirname(os.path.abspath(file))
    default_file_path = os.path.join(current_dir, input_file)
    
    parser = argparse.ArgumentParser(description="🖖")
    parser.add_argument("file_path", type=str, nargs='?',
        default=default_file_path, help="The path to the file containing the input data.")
    
    if not os.path.exists(default_file_path):
        print(f"{default_file_path} does not exist")
        return

    data = open(default_file_path, 'r', encoding='utf-8').read()
    if not data:
        return
    main(parser.parse_args(), data)
    
    return parser.parse_args(), data


def assertions(args, value, *expected_values):
    print(value)
    file_name = args.file_path.split('/')[-1]  # Extract the file name from the path
    for i, expected_value in enumerate(expected_values, start=1):
        if f'input{i}.txt' == file_name:
            assert value == expected_value, f"Expected {expected_value} for {file_name}, but got {value}! 💀"
            break
    else:
        print(f"No expected value provided for {file_name} ⁉️")


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs)  # Call the actual function
        end_time = time.time()
        elapsed_time = end_time - start_time 
        print(f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds ⌛")
        return result
    return wrapper