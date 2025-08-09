import re
from enum import Enum

class I_type(Enum):
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    L_INSTRUCTION = 2

class Parser():

    def __init__(self, program):
        self.program = program
        if len(program) > 0:
            self.has_more_lines = True
        else:
            self.has_more_lines = False
        self.line = ""        
    
    def advance(self):
    # advance(): reads the next instruction. Will search line by line until one is found.
    # Removes comments and whitespace    
        is_instruction = False
        while not is_instruction:
            # Split off the next line of the assembly program
            split_first = self.program.split("\n", 1)
            self.line = split_first[0]
            if len(split_first) > 1:
                self.program = split_first[1]
            else:
                self.program = ""
            # Remove comments from the line
            self.line = re.sub(r"\/\/.*", "", self.line)
            # Strip whitespace
            self.line = self.line.strip()
            # If there is any text remaining, assume it's an instruction
            if len(self.line) > 0:
                is_instruction = True
            if len(self.program) == 0:
                self.has_more_lines = False
                if len(self.line) < 0:
                    break
    
    def instruction_type(self):
        if self.line[0] == "@":
            return I_type.A_INSTRUCTION
        elif self.line[0] == "(":
            return I_type.L_INSTRUCTION
        else:
            return I_type.C_INSTRUCTION
    
    def symbol(self):
        if self.line[0] == "(":
            return re.findall(r"\(([^\(\)]*)\)", self.line)[0]
        else:
            return re.findall(r"@(.*)", self.line)[0]
    
    def dest(self):
        if "=" not in self.line:
            return "null"
        else:
            return self.line.split("=", 1)[0]
            
    def comp(self):
        if "=" in self.line:
            return re.findall(r"=([ADM01+\-!&\|]{1,3})", self.line)[0]
        else:
            return re.findall(r"([ADM01+\-!&\|]{1,3})", self.line)[0]
    
    def jump(self):
        if ";" not in self.line:
            return "null"
        else:
            return re.findall(r";(\w{3})", self.line)[0]



