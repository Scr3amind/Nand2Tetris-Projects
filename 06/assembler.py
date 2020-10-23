import sys

dest_dict = {
    ""      : "000",
    "M"     : "001",
    "D"     : "010",
    "MD"    : "011",
    "A"     : "100",
    "AM"    : "101",
    "AD"    : "110",
    "AMD"   : "111"
}

comp_dict = {
    "0"     : "0101010",
    "1"     : "0111111",
    "-1"    : "0111010",
    "D"     : "0001100",
    "A"     : "0110000",
    "!D"    : "0001101",
    "!A"    : "0110001",
    "-D"    : "0001111",
    "-A"    : "0110011",
    "D+1"   : "0011111",
    "A+1"   : "0110111",
    "D-1"   : "0001110",
    "A-1"   : "0110010",
    "D+A"   : "0000010",
    "D-A"   : "0010011",
    "A-D"   : "0000111",
    "D&A"   : "0000000",
    "D|A"   : "0010101",
    "M"     : "1110000",   
    "!M"    : "1110001",   
    "-M"    : "1110011",   
    "M+1"   : "1110111",   
    "M-1"   : "1110010",   
    "D+M"   : "1000010",   
    "D-M"   : "1010011",   
    "M-D"   : "1000111",   
    "D&M"   : "1000000",   
    "D|M"   : "1010101"   
}

jump_dict = {
    ""      : "000",
    "JGT"   : "001",
    "JEQ"   : "010",
    "JGE"   : "011",
    "JLT"   : "100",
    "JNE"   : "101",
    "JLE"   : "110",
    "JMP"   : "111"
}


symbol_table = {
    "SP"        : "0000000000000000",
    "LCL"       : "0000000000000001",
    "ARG"       : "0000000000000010",
    "THIS"      : "0000000000000011",
    "THAT"      : "0000000000000100",
    "R0"        : "0000000000000000",
    "R1"        : "0000000000000001",
    "R2"        : "0000000000000010",
    "R3"        : "0000000000000011",
    "R4"        : "0000000000000100",
    "R5"        : "0000000000000101",
    "R6"        : "0000000000000110",
    "R7"        : "0000000000000111",
    "R8"        : "0000000000001000",
    "R9"        : "0000000000001001",
    "R10"       : "0000000000001010",
    "R11"       : "0000000000001011",
    "R12"       : "0000000000001100",
    "R13"       : "0000000000001101",
    "R14"       : "0000000000001110",
    "R15"       : "0000000000001111",
    "SCREEN"    : "0100000000000000",
    "KBD"       : "0110000000000000"
    
}

class Parser:
    def __init__(self, file):
      self.file = open(file,"r")

    def generateListOfCommands(self):
        commands = []
        while True:
            line = self.file.readline()

            # EOF
            if(len(line) == 0):
                break

            command = ""
            
            
            for char in line:
                # ignoring white spaces
                if char == ' ':
                    continue
                # ignoring comments
                if char == '/':
                    break
                # ignoring new lines
                if char == '\n':
                    
                    break
                command += char
            
            if len(command) != 0:
                commands.append(command)

        return commands

    def commandType(self, command):
        if command[0] == '@':
            return 'A'
        if command[0] == '(' and command[-1] == ')':
            return 'L'
        if '=' in command or ";" in command:
            return 'C'
        raise Exception("Invalid command: {}".format(command))

    def symbol(self, command):
        if command[0] == '@':
            return command[1:]
        if command[0] == '(':
            return command[1:-1]
    
    def dest(self, command):
        index = command.find('=')
        if index != -1:
            return command[0:index]
        return ""

    def comp(self, command):
        dest_end = command.find("=")
        jmp_begin = command.find(";")

        initial_index = 0
        ending_index = len(command) + 1

        if dest_end != -1:
            initial_index = dest_end + 1
        if jmp_begin != -1:
            ending_index = jmp_begin
        
        return command[initial_index:ending_index]

    def jump(self, command):
        index = command.find(';')
        if index != -1:
            return command[index + 1:]
        return ""

class Code:

    def __init__(self, variableAddress):
      self.variableAddress = variableAddress

    def dest(self, mnemonic):
        dest_bits = dest_dict.get(mnemonic,-1)
        if dest_bits == -1:
            raise Exception("destination invalid {}".format(mnemonic))
        return dest_bits

    def comp(self, mnemonic):
        comp_bits = comp_dict.get(mnemonic,-1)
        if comp_bits == -1:
            raise Exception("comp invalid {}".format(mnemonic))
        return comp_bits
    
    def jump(self, mnemonic):
        jump_bits = jump_dict.get(mnemonic,-1)
        if jump_bits == -1:
            raise Exception("jump invalid {}".format(mnemonic))
        return jump_bits

    def symbol(self, symbol):
        if symbol.isnumeric():
            return self.decToBin(symbol)
        if symbol_table.get(symbol, False) != False:
            return symbol_table[symbol]
        else:
            variable_address = self.decToBin(self.variableAddress)
            symbol_table[symbol] = variable_address
            self.variableAddress += 1
            return variable_address


    def decToBin(self, value):
        dec_Value = int(value)
        bin_value = bin(dec_Value).replace("0b", "")
        missing_zeros = 16 - len(bin_value)
        return "0"*missing_zeros + bin_value

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise Exception("Invalid arguments; assembler.py [program.asm]")

    parser = Parser(sys.argv[1])
    code = Code(16)
    commands = parser.generateListOfCommands()

    output = open(sys.argv[1][:-3] + "hack","w")

    # First Pass
    address = 0

    for command in commands:
        if(parser.commandType(command) == 'L'):
            if(symbol_table.get(command,False) == False):
                symbol = parser.symbol(command)
                symbol_table[symbol] = code.decToBin(address)
        else:
            address += 1


    # Second Pass

    for command in commands:

        machine_instruction = ""

        if(parser.commandType(command) == 'C'):

            dest_mnemonic = parser.dest(command)
            comp_mnemonic = parser.comp(command)
            jump_mnemonic = parser.jump(command)

            machine_instruction = "111" + code.comp(comp_mnemonic) + code.dest(dest_mnemonic) + code.jump(jump_mnemonic)
            
            
        elif(parser.commandType(command) == 'A'):
            symbol_asm = parser.symbol(command)
            machine_instruction = code.symbol(symbol_asm)
        
        if(machine_instruction != ""):
            output.write(machine_instruction)
            output.write("\n")

    output.close()

        
