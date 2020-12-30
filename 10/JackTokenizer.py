class JackTokenizer:

    keywords = [
        "class", "constructor", "function", "method", "field",
        "static", "var", "int", "char", "boolean", "void", "true",
        "false", "null", "this", "let", "do", "if", "else", "while",
        "return"
    ]
    symbols = [
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
        '/', '&', '|', '<', '>', '=', '~'
    ]

    symbol_traductor = {
        '<' : "&lt;",
        '>' : "&gt;",
        '&' : "&amp;"
    }

    ignored_spaces = [
        '\n', '\r' , '\t'
    ]

    def __init__(self, file_name:str):
        self.file_name = file_name
        self.jack_file = open(file_name, "r")
        self.jack_text = self.jack_file.read()
        self.jack_file.close()

       
  
    def tokenize(self):
        program_without_comments = self.remove_comments(self.jack_text)
        program_without_comments = program_without_comments.strip()

        tokens = self.process_tokens(program_without_comments)

        tokens_with_type = self.determine_token_type(tokens)

        self.write_tokens(tokens_with_type)

        return tokens_with_type

    def determine_token_type(self, tokens:list):
        tokens_type = []

        for token in tokens:
            
            if (token in JackTokenizer.keywords):
                tokens_type.append((token,"keyword"))

            elif (token in JackTokenizer.symbols):
                escaped_symbol = self.symbol_traductor.get(token)
                if(escaped_symbol != None):
                    tokens_type.append((escaped_symbol,"symbol"))
                else:
                    tokens_type.append((token,"symbol"))

            elif ('"' in token):
                tokens_type.append((token.replace('"',''), 'stringConstant'))

            elif (token.isdigit()):
                tokens_type.append((token, 'integerConstant'))
            else :
                tokens_type.append((token, 'identifier'))

        return tokens_type
            
    def process_tokens(self, program:str):
        tokens = []
        is_string = False
        current_token = ""
        
        for char in program:
            if (char == '"'):
                if is_string:
                    is_string = False
                    current_token += char
                    continue
                is_string = True

            if is_string:
                current_token += char
                continue

            if char in JackTokenizer.symbols:
                if current_token != " ":
                    tokens.append(current_token.strip())
                tokens.append(char)
                current_token = " "
                continue


            if char in JackTokenizer.ignored_spaces:
                continue
            if char == " ":
                if current_token != " ":
                    tokens.append(current_token.strip())
                current_token = ""

            current_token += char
        
        return tokens
        
    def remove_comments(self, jack_program:str):
        program_without_comments = self.remove_line_comments(jack_program)
        program_without_comments = self.remove_multiline_comments(program_without_comments)
        return program_without_comments

    def remove_line_comments(self, jack_source:str):
        program_lenght = len(jack_source)
        program_without_line_comments = ""
        is_line_comment = False

        for i in range(program_lenght):
            
            if (is_line_comment):
                if ( jack_source[i] == '\n'):
                    is_line_comment = False
                else:
                    continue

            if (jack_source[i] == '/' and jack_source[i + 1] == '/'):
                is_line_comment = True
                continue

            program_without_line_comments += jack_source[i]

        return program_without_line_comments
            
    def remove_multiline_comments(self, jack_source:str):
        program_lenght = len(jack_source)
        program_without_multiline_comments = ""
        is_multiline_comment = False

        for i in range(program_lenght):
            
            if (is_multiline_comment):
                if ( jack_source[i] == '/' and jack_source[i - 1] == '*'):
                    is_multiline_comment = False
                continue

            if (jack_source[i] == '/' and jack_source[i + 1] == '*'):
                is_multiline_comment = True
                continue

            program_without_multiline_comments += jack_source[i]

        return program_without_multiline_comments

    def write_tokens(self, tokens_types:list):
        file = open(self.file_name.replace(".jack","T.xml"), 'w')
       
        file.write("<tokens>\n")
        for token in tokens_types:
            file.write(f"<{token[1]}> {token[0]} </{token[1]}>\n")
        file.write("</tokens>\n")
        
        file.close()