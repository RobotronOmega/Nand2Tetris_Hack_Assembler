import unittest

from parser import Parser, I_type
from transcode import TransCode


class TestAdvance(unittest.TestCase):
    def test_advance(self):
        program = """    @15 // this shouldn't parse
// Neither should this
    D=A"""
        parser = Parser(program)
        parser.advance()
        line1 = parser.line
        #linenum1 = parser.line_number
        has_more1 = parser.has_more_lines
        parser.advance()
        line2 = parser.line
        #linenum2 = parser.line_number
        has_more2 = parser.has_more_lines
        self.assertEqual(line1, "@15")
        self.assertEqual(line2, "D=A")
        #self.assertEqual(linenum1, 1)
        #self.assertEqual(linenum2, 2)
        self.assertEqual(has_more1, True)
        self.assertEqual(has_more2, False)

    def test_instruction_type(self):
        program = """(LOOP)
    @15 // this shouldn't parse
// Neither should this
    D=A
    @0
    D=M-D
    @LOOP
    D;JEQ"""
        parser = Parser(program)
        parser.advance()
        line1type = parser.instruction_type()
        parser.advance()
        line2type = parser.instruction_type()
        parser.advance()
        line3type = parser.instruction_type()
        parser.advance()
        line4type = parser.instruction_type()
        parser.advance()
        line5type = parser.instruction_type()
        parser.advance()
        line6type = parser.instruction_type()
        parser.advance()
        line7type = parser.instruction_type()
        self.assertEqual(line1type, I_type.L_INSTRUCTION)
        self.assertEqual(line2type, I_type.A_INSTRUCTION)
        self.assertEqual(line3type, I_type.C_INSTRUCTION)
        self.assertEqual(line4type, I_type.A_INSTRUCTION)
        self.assertEqual(line5type, I_type.C_INSTRUCTION)
        self.assertEqual(line6type, I_type.A_INSTRUCTION)
        self.assertEqual(line7type, I_type.C_INSTRUCTION)

    def test_extraction(self):
        program = """(LOOP)
    @15 // this shouldn't parse
// Neither should this
    D=A
    @0
    D=M-D
    @LOOP
    D;JEQ"""
        parser = Parser(program)
        tc = TransCode()
        parser.advance()
        line1symbol = parser.symbol()
        parser.advance()
        line2symbol = parser.symbol()
        parser.advance()
        line3dest = parser.dest()
        line3comp = parser.comp()
        line3jump = parser.jump()
        destcode3 = tc.dest(line3dest)
        compcode3 = tc.comp(line3comp)
        jumpcode3 = tc.jump(line3jump)
        parser.advance()
        line4symbol = parser.symbol()
        parser.advance()
        line5dest = parser.dest()
        line5comp = parser.comp()
        line5jump = parser.jump()
        destcode5 = tc.dest(line5dest)
        compcode5 = tc.comp(line5comp)
        jumpcode5 = tc.jump(line5jump)
        parser.advance()
        line6symbol = parser.symbol()
        parser.advance()
        line7dest = parser.dest()
        line7comp = parser.comp()
        line7jump = parser.jump()
        destcode7 = tc.dest(line7dest)
        compcode7 = tc.comp(line7comp)
        jumpcode7 = tc.jump(line7jump)
        self.assertEqual(line1symbol, "LOOP")
        self.assertEqual(line2symbol, "15")
        self.assertEqual(line3dest, "D")
        self.assertEqual(line3comp, "A")
        self.assertEqual(line3jump, "null")
        self.assertEqual(destcode3, "010")
        self.assertEqual(compcode3, "0110000")
        self.assertEqual(jumpcode3, "000")
        self.assertEqual(line4symbol, "0")
        self.assertEqual(line5dest, "D")
        self.assertEqual(line5comp, "M-D")
        self.assertEqual(line5jump, "null")
        self.assertEqual(destcode5, "010")
        self.assertEqual(compcode5, "1000111")
        self.assertEqual(jumpcode5, "000")
        self.assertEqual(line6symbol, "LOOP")
        self.assertEqual(line7dest, "null")
        self.assertEqual(line7comp, "D")
        self.assertEqual(line7jump, "JEQ")
        self.assertEqual(destcode7, "000")
        self.assertEqual(compcode7, "0001100")
        self.assertEqual(jumpcode7, "010")

    

if __name__ == "__main__":
    unittest.main()
