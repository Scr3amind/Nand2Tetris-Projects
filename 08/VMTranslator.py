import sys
import os
import glob

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

        self.static_var_name = ""
        
        self.label_number = 0
        self.functions_stack = ["null"]
        self.return_number = 0


    def setStaticVarName(self, name):
        self.static_var_name = name


 
    def writeInit(self):
        self.output.write("// Bootstrap Code\n")
        self.output.write("@256\n")
        self.output.write("D=A\n")
        self.output.write("@SP\n")
        self.output.write("M=D\n")
        self.writeCall("Sys.init","0")
        
    
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
            self.output.write("@TRUE{}\n".format(self.label_number))
            self.output.write("D;JEQ\n")
            self.output.write("@FALSE{}\n".format(self.label_number))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")
        
        elif command == "gt":
            self.output.write("D=M-D\n")
            self.output.write("@TRUE{}\n".format(self.label_number))
            self.output.write("D;JGT\n")
            self.output.write("@FALSE{}\n".format(self.label_number))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")
        
        elif command == "lt":
           
            self.output.write("D=M-D\n")
            self.output.write("@TRUE{}\n".format(self.label_number))
            self.output.write("D;JLT\n")
            self.output.write("@FALSE{}\n".format(self.label_number))
            self.output.write("0;JMP\n")

            #True Condition
            self.output.write("(TRUE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=-1\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")
            
            #false Condition
            self.output.write("(FALSE{})\n".format(self.label_number))
            self.output.write("@SP\n")
            self.output.write("A=M\n")
            self.output.write("M=0\n")
            self.output.write("@UPDATESP{}\n".format(self.label_number))
            self.output.write("0;JMP\n")

        elif command == "and":
            self.output.write("M=D&M\n")

        elif command == "or":
            self.output.write("M=D|M\n")

        elif command == "not":
            self.output.write("M=!D\n")
        

        # SP++
        self.output.write("(UPDATESP{})\n".format(self.label_number))
        self.output.write("@SP\n")
        self.output.write("M=M+1\n")

        self.label_number += 1   


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
            self.output.write("@{}.{}\n".format(self.static_var_name, arguments[1]))
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

            self.output.write("@{}.{}\n".format(self.static_var_name, arguments[1]))
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

    def writeLabel(self, label):
        self.output.write("// label {} \n".format(label))
        self.output.write("({}${})\n".format(self.functions_stack[-1],label))
    
    def writeGoto(self, label):
        self.output.write("// goto {} \n".format(label))
        self.output.write("@{}${}\n".format(self.functions_stack[-1],label))
        self.output.write("0;JMP\n")

    def writeIf(self, label):
        self.output.write("// if-goto {} \n".format(label))
        # SP--
        self.output.write("@SP\n")
        self.output.write("M=M-1\n")
        self.output.write("A=M\n")
        self.output.write("D=M\n")
        self.output.write("@{}${}\n".format(self.functions_stack[-1],label))
        self.output.write("D;JNE\n")

    def writeCall(self, function_name, num_args):
        self.output.write("// Calling {} with {} args\n".format(function_name, num_args))
        # push return address
        self.output.write("@{}$return-address{}\n".format(self.functions_stack[-1], self.return_number))
        self.output.write("D=A\n")
        # Push value in M[A]
        self.output.write("@SP\n")
        self.output.write("A=M\n")
        self.output.write("M=D\n")
        # Stack++
        self.output.write("@SP\n")
        self.output.write("M=M+1\n")

        #self.__pushSegment("{}$return-address{}".format(self.functions_stack[-1], self.return_number))
        self.__pushSegment("LCL")
        self.__pushSegment("ARG")
        self.__pushSegment("THIS")
        self.__pushSegment("THAT")
        # ARG = SP-n-5
        self.output.write("@{}\n".format(int(num_args)+5)) 
        self.output.write("D=A\n")
        self.output.write("@SP\n")
        self.output.write("D=M-D\n")
        self.output.write("@ARG\n")
        self.output.write("M=D\n")
        # LCL = SP
        self.output.write("@SP\n")
        self.output.write("D=M\n")
        self.output.write("@LCL\n")
        self.output.write("M=D\n")


        #Goto f
        self.output.write("@{}\n".format(function_name))
        self.output.write("0;JMP\n")
        self.writeLabel('return-address{}'.format(self.return_number))

        self.output.write("// End Call\n")

        #update return numbers
        self.return_number += 1

        
        

    def writeReturn(self):
        self.output.write("// Return\n")
        # FRAME = LCL
        self.output.write("@LCL\n")
        self.output.write("D=M\n")
        self.output.write("@FRAME\n")
        self.output.write("M=D\n")
        # RET = *(FRAME - 5)
        self.output.write("@5\n")
        self.output.write("D=A\n")
        self.output.write("@FRAME\n")
        self.output.write("D=M-D\n")
        self.output.write("A=D\n")
        self.output.write("D=M\n")
        self.output.write("@RET\n")
        self.output.write("M=D\n")
        # *ARG = pop()
        self.writePop(['argument','0'])
        # SP = ARG+1
        self.output.write("@ARG\n")
        self.output.write("D=M+1\n")
        self.output.write("@SP\n")
        self.output.write("M=D\n")
        # THAT = *(FRAME-1)
        self.__restoreSegment('THAT',1)
        self.__restoreSegment('THIS',2)
        self.__restoreSegment('ARG',3)
        self.__restoreSegment('LCL',4)
        # goto RET
        self.output.write("@RET\n")
        self.output.write("A=M\n")
        self.output.write("0;JMP\n")

        # Update functions stack
        #self.functions_stack.pop()

    def writeFunction(self, function_name, num_locals):
        # Update functions stack
        self.functions_stack.append(function_name)
        #Comment
        self.output.write("// function {}\n".format(function_name))
        # Label Function
        self.output.write("({})\n".format(function_name))
        

        for _ in range(int(num_locals)):
            self.__initializeLocal()
        
            
    def __initializeLocal(self):
        self.writePush(['constant','0'])

    def __pushSegment(self, segment):
        self.output.write("// pushing {} segment\n".format(segment))
        self.output.write("@{}\n".format(segment))
        self.output.write("D=M\n")
        # Push value in M[A]
        self.output.write("@SP\n")
        self.output.write("A=M\n")
        self.output.write("M=D\n")
        # Stack++
        self.output.write("@SP\n")
        self.output.write("M=M+1\n")
    
    def __restoreSegment(self, segment, number_backward):
        self.output.write("@{}\n".format(number_backward))
        self.output.write("D=A\n")
        self.output.write("@FRAME\n")
        self.output.write("D=M-D\n")
        self.output.write("A=D\n")
        self.output.write("D=M\n")
        self.output.write("@{}\n".format(segment))
        self.output.write("M=D\n")

    def close(self):
        self.output.close()

def generateCode(file_name, code_writer):
    parser = Parser(file_name)
    for command in parser.returnCommands():
        command_type = parser.commandType(command)
        command_args = parser.commandArgs(command)
        if(command_type == "C_PUSH"):
            code_writer.writePush(command_args)
        if(command_type == "C_POP"):
            code_writer.writePop(command_args)
        if(command_type == "C_LABEL"):
            code_writer.writeLabel(command_args[0])
        if(command_type == "C_GOTO"):
            code_writer.writeGoto(command_args[0])
        if(command_type == "C_IF"):
            code_writer.writeIf(command_args[0])
        if(command_type == "C_FUNCTION"):
            code_writer.writeFunction(command_args[0], command_args[1])
        if(command_type == "C_CALL"):
            code_writer.writeCall(command_args[0], command_args[1])
        if(command_type == "C_RETURN"):
            code_writer.writeReturn()
        if(command_type == "C_ARITHMETIC"):
            code_writer.writeArithmetic(command.strip())



if __name__ == "__main__":
    file_name = sys.argv[1]
    
    if(os.path.isfile(file_name)):
        asm_file_name = file_name[:-3]+".asm"
        code_writer = CodeWriter(asm_file_name)
        code_writer.setStaticVarName(os.path.basename(asm_file_name)[:-4])
        
        generateCode(file_name,code_writer)
        
    else:
        asm_name = os.path.basename(os.path.normpath(file_name)) + ".asm"
        asm_name = os.path.join(file_name,asm_name)
        code_writer = CodeWriter(asm_name)
        code_writer.writeInit()
        
        vm_files = glob.glob(file_name+'*.vm')
        for file in vm_files:
            code_writer.setStaticVarName(os.path.basename(file)[:-3])
            generateCode(file,code_writer)
        
    code_writer.close()

    
    
