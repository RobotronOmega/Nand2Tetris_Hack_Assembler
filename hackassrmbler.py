import sys
from pathlib import Path
from parser import Parser, I_type
from transcode import TransCode

if len(sys.argv) < 2:
    print("No asm file provided.")
    sys.exit()

input_path = Path(sys.argv[1])
output_path = Path(f"{input_path.parent}/{input_path.stem}.hack")

try:
    # Open and read the file
    with open(input_path, 'r') as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: File '{input_path}' not found")
    sys.exit()
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

# Initialize parser and transcoder
parser = Parser(content)
tc = TransCode()
hackcode = ""

while parser.has_more_lines:
    parser.advance()
    if parser.has_more_lines:
        if parser.instruction_type() == I_type.A_INSTRUCTION:
            hackcode += f"0{int(parser.symbol()):015b}\n"
        elif parser.instruction_type() == I_type.C_INSTRUCTION:
            hackcode += f"111{parser.comp()}{parser.dest()}{parser.jump()}\n"
hackcode = hackcode[:-1]

with open(output_path, w) as file_stream:
    file_stream.write(hackcode)


