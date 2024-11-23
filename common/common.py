import os
import argparse

from typing import Callable

 
def arg_parse(file: str, input_file: str, main: Callable):
    current_dir = os.path.dirname(os.path.abspath(file))
    default_file_path = os.path.join(current_dir, input_file)
    
    parser = argparse.ArgumentParser(description="🖖")
    parser.add_argument("file_path", type=str, nargs='?',
        default=default_file_path, help="The path to the file containing the input data.")
    return parser.parse_args()
