import os
import sys
from optimize import optimize

input_file = sys.argv[1]
output_file = "./" + os.path.basename(input_file)
if len(sys.argv) >= 3:
	output_file = sys.argv[2]

optimize(input_file, output_file)
