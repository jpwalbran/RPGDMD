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
        MODEPARAM,
        FEATOPT,
        LPAREN,
        RPAREN,
        LCBRACE,
        RCBRACE,
        LNGBRACE,
        RNGBRACE,
        LSBRACE,
        RSBRACE,
        MINUS,
        PLUS,
        DIV,
        TIMES,
        EXP,
        EQ
    }


    def __init__(self):
        self.CNestingLevel = 0
        self.SNestingLevel = 0
        self.NestingLevel = 0
        self.NGNestingLevel = 0

    # Ignore whitespace between tokens
    ignore = ' \t'
    
    ignore_comment = r'[#].*'

    # Define the literals
    literals = {"w", "h"}

    # Shape definitions come at the top
    SHAPE = r'[RCELP]{1}'
    MATERIALID = r'\'[A-Za-z]{1}\'|\.{1}'

    # Handle the mode parameters
    MODEPARAM = r'[A-Za-z]+:'

    # Handle names/identifiers
    NAME = r'[A-Za-z_-]+[A-Za-z0-9_-]*'
    NAME['matdef'] = MATDEF
    
    DESCROP = r'\/\/'

    FEATOPT = r'[DHS-]{1}'

    # Handle String literals
    MULTILINESTRING = r'\"\"\"(.|\n)*\"\"\"'
    STRING = r'\"[^\"]*\"'
    
    # Curly brackets
    LCBRACE = r'\{'
    RCBRACE = r'\}'

    # Square Brackets
    LSBRACE = r'\['
    RSBRACE = r'\]'

    # Parentheses
    LPAREN = r'\('
    RPAREN = r'\)'

    # Angle Brackets
    LNGBRACE = r'\<'
    RNGBRACE = r'\>'
    
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIV = r'\/'
    EXP = r'\^'
    EQ = r'='

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