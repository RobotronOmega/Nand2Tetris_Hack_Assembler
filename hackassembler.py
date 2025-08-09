import sys
from pathlib import Path
from parser import Parser, I_type
from transcode import TransCode
from symboltable import SymbolTable

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
symbols = SymbolTable()
hackcode = ""

# First pass: L_INSTRUCTION parsing
line_number = -1
while parser.has_more_lines:
    parser.advance()
    if parser.line != "":
        if parser.instruction_type() == I_type.A_INSTRUCTION:
            line_number += 1
        elif parser.instruction_type() == I_type.C_INSTRUCTION:
            line_number += 1
        elif parser.instruction_type() == I_type.L_INSTRUCTION:
            symbols.add_entry(parser.symbol(), line_number + 1)

# Second pass: Transcoding
parser = Parser(content)
memory = 16

while parser.has_more_lines:
    parser.advance()
    if parser.line != "":
        if parser.instruction_type() == I_type.A_INSTRUCTION:
            symbol = parser.symbol()
            if symbol[0].isdigit():
                hackcode += f"0{int(symbol):015b}\n"
            else:
                if not symbols.contains(symbol):
                    symbols.add_entry(symbol, memory)
                    memory += 1
                hackcode += f"0{symbols.get_address(symbol):015b}\n"
        elif parser.instruction_type() == I_type.C_INSTRUCTION:
            hackcode += f"111{tc.comp(parser.comp())}{tc.dest(parser.dest())}{tc.jump(parser.jump())}\n"
hackcode = hackcode[:-1]

with open(output_path, 'w') as file_stream:
    file_stream.write(hackcode)


