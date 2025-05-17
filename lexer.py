class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"<{self.type}:{self.value}>"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[0] if source_code else None
        
    def advance(self):
        # Move to next character
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def peek(self):
        if self.position + 1 < len(self.source_code):
            return self.source_code[self.position + 1]
        return None
            
    def skip_whitespace(self):
        # Skip spaces, tabs, newlines
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        self.advance()  # skip first '/'
        self.advance()  # skip second '/'

        # Skip all characters until end of line or end of input
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        # Also skip the newline (Eol)
        if self.current_char == '\n':
            self.advance()

    def get_string(self):
        result = ''
        # Confirm opening ''''
        if not (self.current_char == "'"):
            raise Exception("Invalid string start")
            
        # Skip '''
        self.advance()

        while self.current_char is not None:
            # Check for closing ''''
            if self.current_char == "'" :
                self.advance()
                return Token('STRING', "'"+result+"'")
                
            # Handle escape sequences
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == "'":
                    result += "'"
                else:
                    raise Exception(f"Unknown escape sequence: \\{self.current_char}")
                self.advance()
            elif self.current_char in '();,':
                result += self.current_char
                self.advance()
            elif self.current_char == ' ':
                result += self.current_char
                self.advance()
            elif self.current_char.isalnum() or self.current_char in '+-*<>&.@/:=˜|$!#%^_[]{}"`?':
                result += self.current_char
                self.advance()
            else:
                # Handle unrecognized characters
                raise Exception(f"Invalid character in string: {self.current_char}")


        raise Exception("Unterminated string literal")


            
    def get_identifier(self):
        # Get an identifier or keyword
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a keyword or identifier
        #keywords = {'let', 'within', 'where', 'rec', 'eq', 'aug', 'fn', 'in'}
        #if result in keywords:
            #return Token('KEYWORD', result)
        return Token('IDENTIFIER', result)
    
    def get_number(self):
        # Get a number
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token('INTEGER', int(result))
     
    def get_operator(self):
        # Get an operator 
        result = ''
        while self.current_char and (self.current_char in '+-*<>&.@/:=˜|$!#%^_[]{}"`?'):
            result += self.current_char
            self.advance()
        return Token('OPERATOR', result)
    
    def get_punction(self):
        # Get a punctuation character
        result = ''
        if self.current_char and (self.current_char in '();,'):
            result += self.current_char
            self.advance()
            return Token(result, result)
    
    def get_next_token(self):
        # Main method to get the next token
        while self.current_char:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
                
            # Handle identifiers
            if self.current_char.isalpha():
                return self.get_identifier()
                
            # Handle numbers
            if self.current_char.isdigit():
                return self.get_number()
                
            # Handle operators
            if self.current_char in '+-*<>&.@/:=˜|$!#%^_[]{}"`?':
                return self.get_operator()
            
            # Hanlde punctuations
            if self.current_char in '();,':
                return self.get_punction()
            
            ## Handle strings
            if self.current_char == "'" : 
                return self.get_string()
            
            # Handle an unrecognized character
            raise Exception(f"Invalid character: {self.current_char}")
            
        # End of file
        return Token('EOF', None)
    
    def test_lexer_with_tokens(source):
        """Test the lexer with specific tokens"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
    
        # Print for debugging
        #print("Source:", source)

        ##print("Generated tokens:", [(t.type, t.value) for t in tokens])
        print("Generated tokens:", tokens)

        #print("Expected tokens:", expected_tokens)
    
        # Check if tokens match expected
        #assert len(tokens) == len(expected_tokens), "Token count mismatch"
        #for i, (token, expected) in enumerate(zip(tokens, expected_tokens)):
        #    assert token.type == expected[0], f"Token {i} type mismatch: {token.type} != {expected[0]}"
        #    assert token.value == expected[1], f"Token {i} value mismatch: {token.value} != {expected[1]}"
        #print("Test passed!")
        
    def tokenize(self):
        # Generate all tokens
        tokens = []
        token = self.get_next_token()
        while token.type != 'EOF':
            tokens.append(token)
            token = self.get_next_token()
        return tokens
