from pathlib import Path
import subprocess

# Set the path to your src directory
src_path = Path('../src')

# Set the output file for the extracted messages
output_file = '../src/locale/afoaic.pot'

# Find all .py files in src directory and its subdirectories
py_files = [str(file) for file in src_path.rglob('*.py')]

# Prepare the xgettext command
xgettext_command = [
	'xgettext',
	'--language=Python', 
	'--from-code=UTF-8',
	'--output=' + str(output_file)
] + py_files

# Run the xgettext command using subprocess
subprocess.run(xgettext_command)
