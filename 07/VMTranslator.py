import sys
import os

class Parser:
    def __init__(self, file_name):
        self.file = open(file_name, 'r')

    def returnCommands(self):
        commands = []
        while True:
            line = self.file.readline()
            command = ""

            # EOF
            if len(line) == 0:
                break
            
            line = line.strip()
                  
            for char in line:
                # Ignoring Comments
                if char == '/':
                    break
                if char == '\n':
                    break

                command += char
            
            if len(command) != 0:
                commands.append(command)

        return commands

    def commandType(self, command):

        if "push" in command:
            return "C_PUSH"

        if "pop" in command:
            return "C_POP"

        if "label" in command:
            return "C_LABEL"

        if "if-goto" in command:
            return "C_IF"
        
        if "goto" in command:
            return "C_GOTO"

        if "function" in command:
            return "C_FUNCTION"

        if "return" in command:
            return "C_RETURN"
        
        if "call" in command:
            return "C_CALL"

        return "C_ARITHMETIC"

    def commandArgs(self, command):
        split_spaces = command.split(" ")

        # arithmetic
        if len(split_spaces) == 1:
            return command

        return split_spaces[1:]

class CodeWriter:
    def __init__(self, file_name):
        self.output = open(file_name, 'w')
        self.filename = os.path.basename(file_name)[:-4]
        self.labelNumber = 0
 
    
    def writeArithmetic(self, command):
        self.output.write("// {} \n".format(command))

        self.output.write("@SP\n")
        self.output.write("M=M-1\n")
        self.output.write("A=M\n")
        self.output.write("D=M\n")
        if(command != "neg" and command != "not"):
            self.output.write("@SP\n")
            self.output.write("M=M-1\n")
            self.output.write("A=M\n")

        # Content of D is y

        if command == "add":
            self.output.write("M=M+D\n")
        
        elif command == "sub":
            self.output.write("M=M-D\n")
        
        elif command == "neg":
            self.output.write("M=-D\n")

        elif command == "eq":
            self.output.write("D=D-M\n")
            self.output.write("@TRUE{}\n".format(self.labelNumber))
            self.output.write("D;JEQ\n")
            self.output.write("@FALSE{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")
        
        elif command == "gt":
            self.output.write("D=M-D\n")
            self.output.write("@TRUE{}\n".format(self.labelNumber))
            self.output.write("D;JGT\n")
            self.output.write("@FALSE{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")
        
        elif command == "lt":
            self.output.write("D=M-D\n")
            self.output.write("@TRUE{}\n".format(self.labelNumber))
            self.output.write("D;JLT\n")
            self.output.write("@FALSE{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.labelNumber))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.labelNumber))
            self.output.write("0;JMP\n")

        elif command == "and":
            self.output.write("M=D&M\n")

        elif command == "or":
            self.output.write("M=D|M\n")

        elif command == "not":
            self.output.write("M=!D\n")

        # SP++
        self.output.write("(UPDATESP{})\n".format(self.labelNumber))
        self.output.write("@SP\n")
        self.output.write("M=M+1\n")

        self.labelNumber += 1   


    def writePush(self, arguments):

        # Comment of command
        self.output.write("// push {} {} \n".format(arguments[0], arguments[1]))

        # Constant
        # D = i
        if(arguments[0] != "static" and arguments[0] != "pointer"):
            self.output.write("@{}\n".format(arguments[1]))
            self.output.write("D=A\n")

        if arguments[0] == "local":
            self.output.write("@LCL\n")
            self.output.write("A=D+M\n")
            self.output.write("D=M\n")
            
        
        if arguments[0] == "argument":
            self.output.write("@ARG\n")
            self.output.write("A=D+M\n")
            self.output.write("D=M\n")
            

        if arguments[0] == "this":
            self.output.write("@THIS\n")
            self.output.write("A=D+M\n")
            self.output.write("D=M\n")
            
        if arguments[0] == "that":
            self.output.write("@THAT\n")
            self.output.write("A=D+M\n")
            self.output.write("D=M\n")

        if arguments[0] == "temp":
            self.output.write("@5\n")
            self.output.write("A=D+A\n")
            self.output.write("D=M\n")

        if arguments[0] == "static":
            self.output.write("@{}.{}\n".format(self.filename, arguments[1]))
            self.output.write("D=M\n")
        
        if arguments[0] == "pointer":
            if arguments[1] == '0':
                self.output.write("@THIS\n")
                self.output.write("D=M\n")
            if arguments[1] == '1':
                self.output.write("@THAT\n")
                self.output.write("D=M\n")

            
            
        
        # Push value in M[A]
        self.output.write("@SP\n")
        self.output.write("A=M\n")
        self.output.write("M=D\n")
        # Stack++
        self.output.write("@SP\n")
        self.output.write("M=M+1\n")
           

    def writePop(self, arguments):
        self.output.write("// pop {} {} \n".format(arguments[0], arguments[1]))

        # SP--
        self.output.write("@SP\n")
        self.output.write("M=M-1\n")

        # set i
        if(arguments[0] != "static" and arguments[0] != "pointer"):
            self.output.write("@{}\n".format(arguments[1]))
            self.output.write("D=A\n")
        
        if arguments[0] == "local":
            
            self.output.write("@LCL\n")

        if arguments[0] == "argument":
    
            self.output.write("@ARG\n")
        
        if arguments[0] == "this":
      
            self.output.write("@THIS\n")

        if arguments[0] == "that":
          
            self.output.write("@THAT\n")

        if arguments[0] == "temp":

            self.output.write("@5\n")
            self.output.write("D=D+A\n")

        if arguments[0] == "static":

            self.output.write("@{}.{}\n".format(self.filename, arguments[1]))
            self.output.write("D=A\n")

        if arguments[0] == "pointer":
            if arguments[1] == '0':
                self.output.write("@THIS\n")
                self.output.write("D=A\n")
            if arguments[1] == '1':
                self.output.write("@THAT\n")
                self.output.write("D=A\n")
        
            

        # Saving to address
        if arguments[0] != "temp" and arguments[0] != "pointer":
            self.output.write("D=D+M\n")

        self.output.write("@address\n")
        self.output.write("M=D\n")
            
        # write to segment
        self.output.write("@SP\n")
        self.output.write("A=M\n")
        self.output.write("D=M\n")
        self.output.write("@address\n")
        self.output.write("A=M\n")
        self.output.write("M=D\n")

    def writeLabel(self, arguments):
        self.output.write("// label {} \n".format(arguments[0]))
        self.output.write("({})\n".format(arguments[0]))
    
    def writeGoto(self, arguments):
        self.output.write("// goto {} \n".format(arguments[0]))
        self.output.write("@{}\n".format(arguments[0]))
        self.output.write("0;JMP\n")

    def writeIf(self, arguments):
        self.output.write("// if-goto {} \n".format(arguments[0]))
        # SP--
        self.output.write("@SP\n")
        self.output.write("M=M-1\n")
        self.output.write("A=M\n")
        self.output.write("D=M\n")
        self.output.write("@{}\n".format(arguments[0]))
        self.output.write("D;JNE\n")






    def close(self):
        self.output.close()




if __name__ == "__main__":
    file_name = sys.argv[1]
    parser = Parser(file_name)
    code_writer = CodeWriter(file_name[:-3]+".asm")
    for command in parser.returnCommands():
        command_type = parser.commandType(command)
        command_args = parser.commandArgs(command)
        if(command_type == "C_PUSH"):
            code_writer.writePush(command_args)
        if(command_type == "C_POP"):
            code_writer.writePop(command_args)
        if(command_type == "C_LABEL"):
            code_writer.writeArithmetic(command_args)
        if(command_type == "C_ARITHMETIC"):
            code_writer.writeArithmetic(command)
    
    code_writer.close()