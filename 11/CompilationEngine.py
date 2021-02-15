from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    def __init__(self, filename:str, token_list:list):
        self.token_index = 0
        self.identation_level = 0
        self.tokens = token_list
        self.output_file_name = filename
        self.symbol_table = SymbolTable()
        self.VMWriter = VMWriter(filename.replace(".jack",".vm"))
        self.is_identifier_used = False
        self.current_if_labels = 0
        self.current_while_labels = 0
        pass

    def GetNextToken(self, offset = 0):
        return self.tokens[self.token_index + offset]

    def AdvanceToNextToken(self):
        self.token_index += 1

    def Compile(self):
        self.CompileClass()
        
    def CompileClass(self):

        class_var_types = [
            'static',
            'field'
        ]

        subroutine_types = [
            'constructor',
            'function',
            'method'
        ]

        self.AdvanceToNextToken() # class
        class_name = self.GetNextToken()[0]
        self.symbol_table.class_name = class_name
        self.AdvanceToNextToken() # className
        self.AdvanceToNextToken() # {
        
        while (self.GetNextToken()[0] in class_var_types):
            self.CompileClassVarDec()
        while (self.GetNextToken()[0] in subroutine_types):
            self.CompileSubroutine()

        self.AdvanceToNextToken() # }


    def CompileClassVarDec(self):
        
        self.is_identifier_used = False

        token_kind = self.GetNextToken(0)[0]
        token_type = self.GetNextToken(1)[0]
        token_name = self.GetNextToken(2)[0]
        self.symbol_table.define(token_name, token_type, token_kind)

        self.AdvanceToNextToken() # static | field
        self.AdvanceToNextToken() # type
        self.AdvanceToNextToken() # identifier
        
        
        if(self.GetNextToken()[0] == ','):
            while (self.GetNextToken()[0] != ';'):
                self.AdvanceToNextToken()
                token_name = self.GetNextToken(0)[0]
                self.symbol_table.define(token_name, token_type, token_kind)
                self.AdvanceToNextToken() # identifier


        self.AdvanceToNextToken() # ;

        self.is_identifier_used = True
        
        return 

    def CompileSubroutine(self):

        self.symbol_table.startSubroutine()
        subroutine_type = self.GetNextToken()[0]

        if (subroutine_type == "method"):
            self.CompileMethod()

        elif (subroutine_type == "constructor"):
            self.CompileConstructor()
        
        elif( subroutine_type == "function"):
            self.CompileFunction()
    
        
        return

    def CompileMethod(self):
        class_name = self.symbol_table.class_name
        self.symbol_table.define("this", class_name, "argument")
        
        self.AdvanceToNextToken() # Subroutine type
        self.AdvanceToNextToken() # return type
        
        function_name = self.GetNextToken()[0]
        
        self.AdvanceToNextToken() # subroutine name
        self.AdvanceToNextToken() # (
        
        self.CompileParameterList()
        self.AdvanceToNextToken() # )
        self.VMWriter.writeFunction(f"{class_name}.{function_name}")
        self.CompileMethodBody()




    def CompileConstructor(self):
        class_name = self.symbol_table.class_name
        
        self.AdvanceToNextToken() # Subroutine type
        self.AdvanceToNextToken() # return type
        
        function_name = self.GetNextToken()[0]
        
        self.AdvanceToNextToken() # subroutine name
        self.AdvanceToNextToken() # (
        
        self.CompileParameterList()
        self.AdvanceToNextToken() # )
        self.VMWriter.writeFunction(f"{class_name}.{function_name}")
        self.CompileConstructorBody()

        

    def CompileFunction(self):
        class_name = self.symbol_table.class_name
        
        self.AdvanceToNextToken() # Subroutine type
        self.AdvanceToNextToken() # return type
        
        function_name = self.GetNextToken()[0]
        
        self.AdvanceToNextToken() # subroutine name
        self.AdvanceToNextToken() # (
        
        self.CompileParameterList()
        self.AdvanceToNextToken() # )
        self.VMWriter.writeFunction(f"{class_name}.{function_name}")
        self.CompileFunctionBody()


    def CompileParameterList(self):

        if (self.GetNextToken()[0] == ')'):
            return

        self.is_identifier_used = False

        token_kind = "argument"
        token_type = self.GetNextToken(0)[0]
        token_name = self.GetNextToken(1)[0]
        self.symbol_table.define(token_name, token_type, token_kind)
        
        self.AdvanceToNextToken() # type
        self.AdvanceToNextToken() # varName



        
        while(self.GetNextToken()[0] != ')'):
            self.AdvanceToNextToken() # , 
            token_type = self.GetNextToken(0)[0]
            token_name = self.GetNextToken(1)[0]
            self.symbol_table.define(token_name, token_type, token_kind)
            
            self.AdvanceToNextToken() # token type 
            self.AdvanceToNextToken() # token name 


        self.is_identifier_used = True

        return


    def CompileFunctionBody(self):
        
        self.AdvanceToNextToken() # {
        n_locals = 0
        while(self.GetNextToken()[0] == "var"):
            n_locals += self.CompileVarDec()

        self.VMWriter.writeFunctionLocals(n_locals)
        self.CompileStatements()

        self.AdvanceToNextToken() # }

        return

    def CompileMethodBody(self):
        
        self.AdvanceToNextToken() # {
        n_locals = 0
        while(self.GetNextToken()[0] == "var"):
            n_locals += self.CompileVarDec()

        self.VMWriter.writeFunctionLocals(n_locals)
        self.VMWriter.writePush("argument", 0)
        self.VMWriter.writePop("pointer", 0)
        self.CompileStatements()

        self.AdvanceToNextToken() # }

        return

    def CompileConstructorBody(self):
        
        self.AdvanceToNextToken() # {
        n_locals = 0
        while(self.GetNextToken()[0] == "var"):
            n_locals += self.CompileVarDec()

        self.VMWriter.writeFunctionLocals(n_locals)
        number_of_fields = self.symbol_table.varCount("field")
        self.VMWriter.writePush("constant", number_of_fields)
        self.VMWriter.writeCall("Memory.alloc", 1)
        self.VMWriter.writePop("pointer",0)

        self.CompileStatements()

        self.AdvanceToNextToken() # }

        return
    
    def CompileVarDec(self):

        self.is_identifier_used = False
        token_kind = "local"
        token_type = self.GetNextToken(1)[0]
        
        self.AdvanceToNextToken() # var
        self.AdvanceToNextToken() # type
        inline_locals = 0

        # same line var declarations
        while True:
            token_name = self.GetNextToken(0)[0]
            self.symbol_table.define(token_name, token_type, token_kind)
            self.AdvanceToNextToken() # varName
            inline_locals += 1
            if (self.GetNextToken()[0] != ','):
                break
            self.AdvanceToNextToken() # ,
        self.AdvanceToNextToken() #;

        self.is_identifier_used = True
        return inline_locals

    def CompileStatements(self):
        statement_types = [
            "let", "if", "while", "do", "return"
        ]

        while(self.GetNextToken()[0] in statement_types):
            if (self.GetNextToken()[0] == "let"):
                self.CompileLet()
            elif (self.GetNextToken()[0] == "if"):
                self.CompileIf()
            elif (self.GetNextToken()[0] == "while"):
                self.CompileWhile()
            elif (self.GetNextToken()[0] == "do"):
                self.CompileDo()
            elif (self.GetNextToken()[0] == "return"):
                self.CompileReturn()


        return
        
    def CompileDo(self):
        self.AdvanceToNextToken() #do
        self.CompileSubroutineCall()
        self.AdvanceToNextToken() #;
        self.VMWriter.writePop("temp",0)

        return

    def CompileLet(self):
        self.AdvanceToNextToken() # let
        
        if(self.IsVarArray()):
            self.CompileArrayAccess()
        
        else:
            var_name = self.GetNextToken()[0]
            var_index = self.symbol_table.indexOf(var_name)
            var_segment = self.symbol_table.kindOf(var_name)
            if(var_segment == "field"):
                var_segment = "this"

            self.AdvanceToNextToken() # varName
            
            self.AdvanceToNextToken() # =
            self.CompileExpression()
            self.AdvanceToNextToken() # ;
            self.VMWriter.writePop(var_segment, var_index)


        return

    def CompileWhile(self):
        L1, L2 = self.GetCurrentWhileLabels()

        self.VMWriter.writeLabel(L1)

        self.AdvanceToNextToken() # while
        self.AdvanceToNextToken() # (
        self.CompileExpression()
        self.AdvanceToNextToken() # )
        self.VMWriter.writeArithmetic("not")
        self.VMWriter.writeIf(L2)
        self.AdvanceToNextToken() # {
        self.CompileStatements()
        self.AdvanceToNextToken() # }
        self.VMWriter.writeGoto(L1)
        self.VMWriter.writeLabel(L2)

        return

    def GetCurrentWhileLabels(self):
        L1 = f"WHILE_EXP{self.current_while_labels}"
        L2 = f"WHILE_END{self.current_while_labels}"
        self.current_while_labels += 1
        return (L1,L2)

    def CompileReturn(self):
        is_void = True
        self.AdvanceToNextToken() # return
        if(self.GetNextToken()[0] != ';'):
            is_void = False
            self.CompileExpression()
        
        self.AdvanceToNextToken() #;
        if(is_void):
            self.VMWriter.writePush("constant",0)
        
        self.VMWriter.writeReturn()


        return

    def CompileIf(self):

        L1,L2 = self.GetCurrentIfLabels()

        self.AdvanceToNextToken() # if
        self.AdvanceToNextToken() # (
        self.CompileExpression()
        self.AdvanceToNextToken() # )
        self.VMWriter.writeArithmetic("not")
        self.VMWriter.writeIf(L1)
        self.AdvanceToNextToken() # {
        self.CompileStatements()
        self.AdvanceToNextToken() # }
        self.VMWriter.writeGoto(L2)
        self.VMWriter.writeLabel(L1)
        if (self.GetNextToken()[0] == "else"):
            self.AdvanceToNextToken() # else
            self.AdvanceToNextToken() # {
            self.CompileStatements()
            self.AdvanceToNextToken() # }
        self.VMWriter.writeLabel(L2)
        
        return

    def GetCurrentIfLabels(self):
        L1 = f"IF_TRUE{self.current_if_labels}"
        L2 = f"IF_FALSE{self.current_if_labels}"
        self.current_if_labels += 1
        return (L1,L2)

    def CompileExpression(self):
        operator_to_command = {
            '+' : "add", 
            '-' : "sub", 
            '*' : "mult", 
            '/' : "div", 
            "&amp;" : "and", 
            '|' : "or", 
            "&lt;" : "lt", 
            "&gt;" : "gt", 
            '=': "eq"
        }

        self.CompileTerm()
        while(self.GetNextToken()[0] in operator_to_command.keys()):
            operator = self.GetNextToken()[0]
            self.AdvanceToNextToken() # op
            self.CompileTerm()
            
            if (operator == '*'):
                self.VMWriter.writeCall("Math.multiply", 2)
            elif(operator == '/'):
                self.VMWriter.writeCall("Math.divide", 2)
            else:
                self.VMWriter.writeArithmetic(operator_to_command[operator])


        return

    def CompileTerm(self):
        u_operators_to_command = {
            '-' : "neg",
            '~' : "not"
        }
        

        if (self.IsUnaryOperator()):
            u_operator = self.GetNextToken()[0]
            self.AdvanceToNextToken() # unary op
            self.CompileTerm()
            self.VMWriter.writeArithmetic(u_operators_to_command[u_operator])
                
        elif (self.IsExpressionParentheses()):
            self.AdvanceToNextToken() # (
            self.CompileExpression()
            self.AdvanceToNextToken() # )

        elif (self.IsSubroutineCall()):
            self.CompileSubroutineCall()

        elif (self.IsVarArray()):
            self.CompileArrayAccess()

        elif (self.IsIntegerConstant()):
            self.CompileIntegerConstant()

        elif (self.IsStringConstant()):
            self.CompileStringConstant()

        elif (self.IsKeywordConstant()):
            self.CompileKeywordConstant()

        else:
            self.CompileVarName()


        return

    def IsIntegerConstant(self):
        return self.GetNextToken()[0].isdigit()

    def IsStringConstant(self):
        token_type = self.GetNextToken()[1]
        return (token_type == "stringConstant")

    def IsKeywordConstant(self):
        keyword_constants = (
            "true", "false", "null", "this"
        )

        return (self.GetNextToken()[0] in keyword_constants)

    def IsUnaryOperator(self):
        u_operators= {
            '-', '~' 
        }
        return (self.GetNextToken()[0] in u_operators)

    def IsExpressionParentheses(self):
        return (self.GetNextToken()[0] == '(')

    def IsSubroutineCall(self):
        # subroutineName(expresionList)
        subroutine_cond1 = self.GetNextToken(1)[0] == '('
        # className|varName.subroutineName(expressionList)
        subroutine_cond2 = self.GetNextToken(1)[0] == '.' and self.GetNextToken(3)[0] == '('
        return subroutine_cond1 or subroutine_cond2

    def IsVarArray(self):
        return self.GetNextToken(1)[0] == '['

    def CompileIntegerConstant(self):
        self.VMWriter.writePush("constant",self.GetNextToken()[0])
        self.AdvanceToNextToken()

    def CompileStringConstant(self):
        string_constant = self.GetNextToken()[0]
        self.AdvanceToNextToken()
        self.VMWriter.writePush("constant", len(string_constant))
        self.VMWriter.writeCall("String.new",1)
        for c in string_constant:
            self.VMWriter.writePush("constant", ord(c))
            self.VMWriter.writeCall("String.appendChar",2)

    def CompileKeywordConstant(self):
        if(self.GetNextToken()[0] == "false"):
            self.VMWriter.writePush("constant", 0)
        elif(self.GetNextToken()[0] == "null"):
            self.VMWriter.writePush("constant", 0)
        elif(self.GetNextToken()[0] == "true"):
            self.VMWriter.writePush("constant", 1)
            self.VMWriter.writeArithmetic("neg")
        elif(self.GetNextToken()[0] == "this"):
            self.VMWriter.writePush("pointer", 0)
        self.AdvanceToNextToken()

    def CompileVarName(self):
        segment = self.symbol_table.kindOf(self.GetNextToken()[0])
        index = self.symbol_table.indexOf(self.GetNextToken()[0])
        if(segment == "field"):
            segment = "this"
        self.VMWriter.writePush(segment, index)
        self.AdvanceToNextToken()

    def CompileExpressionList(self):
        n_args = 0

        while (self.GetNextToken()[0] != ')'):
            self.CompileExpression()
            n_args += 1
            while (self.GetNextToken()[0] == ','):
                self.AdvanceToNextToken() # ,
                self.CompileExpression()
                n_args += 1

        return n_args

    def CompileSubroutineCall(self):
        function_name = self.GetNextToken()[0]
        n_args = 0
        var_name = self.GetNextToken()[0]
        
        if(self.symbol_table.contains(var_name)):
            self.CompileVarName()
            n_args += 1
            function_name = self.symbol_table.typeOf(var_name)

        else:
            self.AdvanceToNextToken() # subroutineName | className | varName
        
        if (self.GetNextToken()[0] == '('):
            self.AdvanceToNextToken() # (
            # Method
            self.VMWriter.writePush("pointer",0)
            n_args += 1
            function_name = self.symbol_table.class_name +'.'+ function_name
            n_args += self.CompileExpressionList()
            self.AdvanceToNextToken() # )
        elif (self.GetNextToken()[0] == '.'):
            self.AdvanceToNextToken() # .
            function_name += "." + self.GetNextToken()[0]
            self.AdvanceToNextToken() # SubroutineName
            self.AdvanceToNextToken() # (
            n_args += self.CompileExpressionList()
            self.AdvanceToNextToken() # )
        
        self.VMWriter.writeCall(function_name, n_args)

    def CompileArrayAccess(self):
        # push arr base address
        self.CompileVarName() # varName
        self.AdvanceToNextToken() # [
        self.CompileExpression()
        self.AdvanceToNextToken() # ]
        self.VMWriter.writeArithmetic("add")
        
        if(self.GetNextToken()[0] == '='):
            self.AdvanceToNextToken()
            self.CompileExpression()
            self.AdvanceToNextToken() # ;
            self.VMWriter.writePop("temp",0)
            self.VMWriter.writePop("pointer",1)
            self.VMWriter.writePush("temp",0)
            self.VMWriter.writePop("that",0)

        else:
            self.VMWriter.writePop("pointer",1)
            self.VMWriter.writePush("that",0)

        

            