import os
import re
import shutil

# path = "src/bonus/validateChecksum.s"
path = "bonus/validateChecksum2.s"

original_file = "src/validateChecksum.s"
temp_file = "src/validateChecksum.s.original"

if not os.path.isfile(path):
    print(f"File {path} does not exist.")
    exit(1)
    
with open(path, "r") as f:
    content = f.read()
    
content = re.sub(r"#.*", "", content)

def print_offending_line(regex, content):
    for i, line in enumerate(content.splitlines()):
        if re.search(regex, line):
            print(f"Line {i + 1}: {line.strip()}")
    
memory_instruction_regex = r"\b(sw|ecall)\b"
if re.search(memory_instruction_regex, content):
    print(f"File {path} contains forbidden instructions that might touch memory:")
    print_offending_line(memory_instruction_regex, content)
    exit(1)

def strip_whitespace(s):
    return re.sub(r"\s+", "", s, flags=re.DOTALL | re.MULTILINE)
    
allowed_data_segment = """
	.data
	.globl validate_checksum
	.text
"""
allowed_data_segment = strip_whitespace(allowed_data_segment)
data_segment_regex = r"\.data(.*?)\.text"
data_segment = re.search(data_segment_regex, content, re.DOTALL)
if not data_segment:
    print("No valid .data segment found.")
    exit(1)
data_segment = strip_whitespace(data_segment.group(0))
if data_segment != allowed_data_segment:
    print("The .data segment does not match the allowed .data segment.")
    exit(1)
import_regex = r"\b(import|include)\b"
if re.search(import_regex, content):
    print(f"File {path} contains forbidden import statements:")
    print_offending_line(import_regex, content)
    exit(1)

label_regex = r"^\s*(\w+):"
labels = set(re.findall(label_regex, content, re.MULTILINE))
content_without_data = re.sub(data_segment_regex, "", content, flags=re.DOTALL)
lines = [line for line in content_without_data.splitlines() if line.strip() and not re.match(label_regex, line)]
# no pc, sp, gp
registers = ["zero", "ra"] + [f"t{i}" for i in range(7)] + [f"s{i}" for i in range(12)] + [f"a{i}" for i in range(8)]
for i, line in enumerate(lines):
    parts = line.split()
    if len(parts) < 2:
        print(f"Invalid instruction format in line {i + 1}: {line.strip()}")
        exit(1)
    arguments = parts[1:]
    for arg in arguments:
        arg = arg.strip(", ")
        # if number, skip
        if re.match(r"^-?\d+$", arg):
            continue
        match = re.match(r"\d+\((\w+)\)", arg)
        if match:
            arg = match.group(1)
        if arg not in registers:
            if arg in labels:
                continue
            print(f"Forbidden register/label used in line {i + 1}: {line.strip()}")

# tests run with file replaced
if os.path.isfile(temp_file):
    print(f"Temporary file {temp_file} already exists. Please remove it and run the script again.")
    exit(1)
    
os.rename(original_file, temp_file)
shutil.copy(path, original_file)

# find all test folders
test_folders = [d for d in os.listdir("tests") if os.path.isdir(os.path.join("tests", d))]
exit_code = 0
output = ""
try:
    process = os.popen(f"python run_tests.py -d {' '.join(test_folders)}")
    output = process.read()
    exit_code = process.close()
except Exception as e:
    print(f"An error occurred while running the tests: {e}")
    exit(1)
finally:
    # restore original file
    if os.path.isfile(temp_file):
        os.rename(temp_file, original_file)
    else:
        print(f"Temporary file {temp_file} not found. Original file might not have been restored. Please check src/validateChecksum.s")
        exit(1)
if exit_code is not None:
    print(f"Tests failed with exit code {exit_code}. Output:")
    print(output)
    exit(1)

print("Bonus file is correct (according to tests) and does not contain forbidden instructions or imports.")