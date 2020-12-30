class CompilationEngine:
    def __init__(self, filename:str, token_list:list):
        self.token_index = 0
        self.identation_level = 0
        self.tokens = token_list
        self.output_file_name = filename
        pass

    def GetNextToken(self):
        return self.tokens[self.token_index]

    def WriteNextToken(self):
        token = self.GetNextToken()[0]
        token_type = self.GetNextToken()[1]
        
        self.output_file.write("  "*self.identation_level)
        self.output_file.write(f"<{token_type}> {token} </{token_type}>\n")

        self.token_index += 1

    def WriteToFile(self, text:str):
        self.output_file.write("  "*self.identation_level)
        self.output_file.write(f"{text}\n")

    def CompileWithFormat(self, compile_function, tag_name:str):
        self.WriteToFile(f"<{tag_name}>")
        self.identation_level += 1
        compile_function()
        self.identation_level -= 1
        self.WriteToFile(f"</{tag_name}>")
        return


    def Compile(self):
        self.output_file = open(self.output_file_name.replace(".jack",".xml"), 'w')
        self.CompileWithFormat(self.CompileClass,"class")
        self.output_file.close()


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

        self.WriteNextToken() # class
        self.WriteNextToken() # className
        self.WriteNextToken() # {
        
        while (self.GetNextToken()[0] in class_var_types):
            self.CompileWithFormat(self.CompileClassVarDec,"classVarDec")
        while (self.GetNextToken()[0] in subroutine_types):
            self.CompileWithFormat(self.CompileSubroutine,"subroutineDec")

        self.WriteNextToken() # }


    def CompileClassVarDec(self):

        self.WriteNextToken() # static | field
        self.WriteNextToken() # type
        self.WriteNextToken() # identifier
        
        if(self.GetNextToken()[0] == ','):
            while (self.GetNextToken()[0] != ';'):
                self.WriteNextToken() # identifier


        self.WriteNextToken() # ;
        
        return 

    def CompileSubroutine(self):


        self.WriteNextToken() # Subroutine type

        self.WriteNextToken() # return type
        self.WriteNextToken() # subroutine name
        self.WriteNextToken() # (

        self.CompileWithFormat(self.CompileParameterList,"parameterList")

        self.WriteNextToken() # )

        self.CompileWithFormat(self.CompileSubroutineBody,"subroutineBody")
        
        return

    def CompileParameterList(self):

        if (self.GetNextToken()[0] == ')'):
            return

        
        self.WriteNextToken() # type
        self.WriteNextToken() # varName

        
        while(self.GetNextToken()[0] != ')'):
            self.WriteNextToken()

        return 

    def CompileSubroutineBody(self):
        
        self.WriteNextToken() # {

        while(self.GetNextToken()[0] == "var"):
            self.CompileWithFormat(self.CompileVarDec,"varDec")

        self.CompileWithFormat(self.CompileStatements,"statements")

        self.WriteNextToken() # }

        return
    
    def CompileVarDec(self):

        self.WriteNextToken() # var
        self.WriteNextToken() # type

        # same line var declarations
        while True:
            self.WriteNextToken() # varName
            if (self.GetNextToken()[0] != ','):
                break
            self.WriteNextToken() # ,
        self.WriteNextToken() #;
        return 



    def CompileStatements(self):
        statement_types = [
            "let", "if", "while", "do", "return"
        ]

        while(self.GetNextToken()[0] in statement_types):
            if (self.GetNextToken()[0] == "let"):
                self.CompileWithFormat(self.CompileLet,"letStatement")
            elif (self.GetNextToken()[0] == "if"):
                self.CompileWithFormat(self.CompileIf,"ifStatement")
            elif (self.GetNextToken()[0] == "while"):
                self.CompileWithFormat(self.CompileWhile,"whileStatement")
            elif (self.GetNextToken()[0] == "do"):
                self.CompileWithFormat(self.CompileDo,"doStatement")
            elif (self.GetNextToken()[0] == "return"):
                self.CompileWithFormat(self.CompileReturn,"returnStatement")


        return
        

    def CompileDo(self):
        self.WriteNextToken() #do
        self.CompileSubroutineCall()
        self.WriteNextToken() #;

        return

    def CompileLet(self):
        self.WriteNextToken() # let
        self.WriteNextToken() # varName

        if(self.GetNextToken()[0] == '['):
            self.WriteNextToken() # [
            self.CompileWithFormat(self.CompileExpression,'expression')
            self.WriteNextToken() # ]
        
        self.WriteNextToken() # =
        self.CompileWithFormat(self.CompileExpression,'expression')
        self.WriteNextToken() # ;


        return


    def CompileWhile(self):
        self.WriteNextToken() # while
        self.WriteNextToken() # (
        self.CompileWithFormat(self.CompileExpression, "expression")
        self.WriteNextToken() # )
        self.WriteNextToken() # {
        self.CompileWithFormat(self.CompileStatements, "statements")
        self.WriteNextToken() # }

        return

    def CompileReturn(self):
        self.WriteNextToken() # return
        if(self.GetNextToken()[0] != ';'):
            self.CompileWithFormat(self.CompileExpression, "expression")
        
        self.WriteNextToken() #;


        return

    def CompileIf(self):
        self.WriteNextToken() # if
        self.WriteNextToken() # (
        self.CompileWithFormat(self.CompileExpression,"expression")
        self.WriteNextToken() # )
        self.WriteNextToken() # {
        self.CompileWithFormat(self.CompileStatements, "statements")
        self.WriteNextToken() # }
        if (self.GetNextToken()[0] == "else"):
            self.WriteNextToken() # else
            self.WriteNextToken() # {
            self.CompileWithFormat(self.CompileStatements, "statements")
            self.WriteNextToken() # }
        
        return

    def CompileExpression(self):
        operators = [
            '+', '-', '*', '/', "&amp;", '|', "&lt;", "&gt;", '='
        ]
        self.CompileWithFormat(self.CompileTerm,"term")
        while(self.GetNextToken()[0] in operators):
            self.WriteNextToken() # op
            self.CompileWithFormat(self.CompileTerm,"term")


        return

    def CompileTerm(self):
        unary_operators = [
            '-', '~'
        ]

        if (self.GetNextToken()[0] in unary_operators):
            self.WriteNextToken() # unary op
            self.CompileWithFormat(self.CompileTerm,"term")
        # ( Expression )        
        elif (self.GetNextToken()[0] == '('):
            self.WriteNextToken() # (
            self.CompileWithFormat(self.CompileExpression,"expression")
            self.WriteNextToken() # )

        else:
            self.WriteNextToken() # integerConstant | stringConstant | keywordConstant | varName

            if (self.GetNextToken()[0] == '['):
                self.WriteNextToken() # [
                self.CompileWithFormat(self.CompileExpression,"expression")
                self.WriteNextToken() # ]

            elif (self.GetNextToken()[0] == '('):
                self.WriteNextToken() # (
                self.CompileWithFormat(self.CompileExpressionList,"expressionList")
                self.WriteNextToken() # )
            
            elif (self.GetNextToken()[0] == '.'):
                self.WriteNextToken() # .
                self.WriteNextToken() # subroutine Name
                self.WriteNextToken() # (
                self.CompileWithFormat(self.CompileExpressionList,"expressionList")
                self.WriteNextToken() # )

            

        return

    def CompileExpressionList(self):

        while (self.GetNextToken()[0] != ')'):
            self.CompileWithFormat(self.CompileExpression,"expression")
            while (self.GetNextToken()[0] == ','):
                self.WriteNextToken() # ,
                self.CompileWithFormat(self.CompileExpression,"expression")

        return

    def CompileSubroutineCall(self):
        self.WriteNextToken() # subroutineName | className | varName
        if (self.GetNextToken()[0] == '('):
            self.WriteNextToken() # (
            self.CompileWithFormat(self.CompileExpressionList, "expressionList")
            self.WriteNextToken() # )
        elif (self.GetNextToken()[0] == '.'):
            self.WriteNextToken() # .
            self.WriteNextToken() # SubroutineName
            self.WriteNextToken() # (
            self.CompileWithFormat(self.CompileExpressionList, "expressionList")
            self.WriteNextToken() # )


    