import os
import argparse

import time
from functools import wraps

from typing import Callable

 
def arg_parse(file: str, input_file: str, main: Callable):
    current_dir = os.path.dirname(os.path.abspath(file))
    default_file_path = os.path.join(current_dir, input_file)
    
    parser = argparse.ArgumentParser(description="🖖")
    parser.add_argument("file_path", type=str, nargs='?',
        default=default_file_path, help="The path to the file containing the input data.")
    return parser.parse_args()


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the actual function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds ⌛")
        return result  # Return the function's result
    return wrapper