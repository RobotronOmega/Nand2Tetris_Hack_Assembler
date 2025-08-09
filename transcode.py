class TransCode():
    
    def dest(self, str):
        out = ""
        if "A" in str:
            out += "1"
        else:
            out += "0"
        if "D" in str:
            out += "1"
        else:
            out += "0"
        if "M" in str:
            out += "1"
        else:
            out += "0"
        return out
    
    def comp(self, str):
        out = ""
        if "M" in str:
            out += "1"
        else:
            out += "0"
        match(str):
            case "0":
                out += "101010"
            case "1":
                out += "111111"
            case "-1":
                out += "111010"
            case "D":
                out += "001100"
            case "A" | "M":
                out += "110000"
            case "!D":
                out += "001101"
            case "!A" | "!M":
                out += "110001"
            case "-D":
                out += "001111"
            case "-A" | "-M":
                out += "110011"
            case "D+1":
                out += "011111"
            case "A+1" | "M+1":
                out += "110111"
            case "D-1":
                out += "001110"
            case "A-1" | "M-1":
                out += "110010"
            case "D+A" | "D+M":
                out += "000010"
            case "D-A" | "D-M":
                out += "010011"
            case "A-D" | "M-D":
                out += "000111"
            case "D&A" | "D&M":
                out += "000000"
            case "D|A" | "D|M":
                out += "010101"
        return out
    
    def jump(self, str):
        if str == "null":
            return "000"
        else:
            match(str):
                case "JGT":
                    return "001"
                case "JEQ":
                    return "010"
                case "JGE":
                    return "011"
                case "JLT":
                    return "100"
                case "JNE":
                    return "101"
                case "JLE":
                    return "110"
                case "JMP":
                    return "111"
                
