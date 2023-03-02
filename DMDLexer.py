from sly import Lexer

class DMDLexer(Lexer):

    # List of possible tokens
    tokens = {
        MATERIALID,
        NAME,
        STRING,
        MULTILINESTRING,
        SHAPE,
        MATDEF,
        NUMBER,
        MATDEF,
        DESCROP,
        DIV,
        MODEPARAM,
        MODE
    }


    def __init__(self):
        self.CNestingLevel = 0
        self.SNestingLevel = 0
        self.NestingLevel = 0
        self.NGNestingLevel = 0

    # Ignore whitespace between tokens
    ignore = ' \t'
    
    # Ignore comments
    ignore_comment = r'[#].*'

    # Define the literals/keywords
    literals = {"+", "-", "*", "^", "(", ")", "[", "]", "{", "}", "=", "<", ">"}

    # Shape definitions come at the top
    SHAPE = r'[RCELP]'
    MATERIALID = r'\'[A-Za-z]{1}\'|\.{1}'

     # Handle the mode parameters
    MODEPARAM = r'[A-Za-z]+:'

    # Handle names/identifiers
    NAME = r'[A-Za-z_-]+[A-Za-z0-9_-]*'
    NAME['matdef'] = MATDEF
    
    DESCROP = r'\/\/'

    DIV = r'\/'

    # Handle String literals
    MULTILINESTRING = r'\"\"\"(.|\n)*\"\"\"'
    STRING = r'\"[^\"]*\"'

    # Handle rectangle modes
    MODE = r'\'(c|bl|br|tl|tr|cx|cy)\''
    
    # Handle bracket nesting
    
    # Curly brackets
    @_(r'\{')
    def LCBRACE(self, t):
        t.type = '{'
        self.CNestingLevel += 1
        return t
    
    @_(r'\}')
    def RCBRACE(self, t):
        t.type = '}'
        self.CNestingLevel -= 1
        return t
    
    # Square Brackets
    @_(r'\[')
    def LSBRACE(self, t):
        t.type = '['
        self.SNestingLevel += 1
        return t

    @_(r'\]')
    def RSBRACE(self, t):
        t.type = ']'
        self.SNestingLevel -= 1
        return t

    # Parentheses
    @_(r'\(')
    def LBRACE(self, t):
        t.type = '('
        self.NestingLevel += 1
        return t
    
    @_(r'\)')
    def RBRACE(self, t):
        t.type = ')'
        self.NestingLevel -= 1
        return t

    # Angle Brackets
    @_(r'\<')
    def LNGBRACE(self, t):
        t.type = "<"
        self.NGNestingLevel += 1
        return t
    
    @_(r'\>')
    def RNGBRACE(self, t):
        t.type = ">"
        self.NGNestingLevel -= 1
        return t

    # Convert all numbers to ints
    @_(r'[0-9]+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Keep a line count
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    # General error handling
    def error(self, t):
        print(f"Illegal character {t.value[0]} at line {self.lineno}")
        self.index += 1

if __name__ == '__main__':
    with open("exampleIn.txt") as f:
        data = f.read()
    lexer = DMDLexer()
    for tok in lexer.tokenize(data):
        print(tok)