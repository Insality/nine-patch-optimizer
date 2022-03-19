import os
import sys
from optimize import optimize

input_directory = sys.argv[1]
current_directory = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".png"):
            input_file = os.path.join(root, file)
            relative_path = os.path.relpath(input_file, input_directory)
            output_file = os.path.join(current_directory, "output", relative_path)
            optimize(input_file, output_file)
