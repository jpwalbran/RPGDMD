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
        EQ,
        HEIGHT,
        WIDTH
    }

    # Ignore whitespace between tokens
    ignore = ' \t'
    
    ignore_comment = r'[#].*'

    # Shape definitions come at the top
    SHAPE = r'[RCELP]{1}'
    
    # Handle the mode parameters
    MODEPARAM = r'[A-Za-z]+:'

    # Handle names/identifiers
    NAME = r'[A-Za-z_]+[A-Za-z0-9_]*'
    NAME['matdef'] = MATDEF
    NAME['w'] = WIDTH
    NAME['h'] = HEIGHT
     
    DESCROP = r'\/\/'

    FEATOPT = r'[DHS~]{1}'

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
    TIMES = r'\*'
    MINUS = r'\-'
    DIV = r'\/'
    EXP = r'\^'
    EQ = r'='

    # Strip quotes out of materialids and strings
    @_(r'\'[A-Za-z]{1}\'|\.{1}')
    def MATERIALID(self, t):
        if t.value == '.':
            t.value = '.'
        else:
            t.value = t.value[1:-1] # Remove the first and last characters, which are always quotes
        return t

    @_(r'\"\"\"(.|\n)*\"\"\"')
    def MULTILINESTRING(self, t):
        t.value = t.value[3:-3] # Remove the first and last three characters from the literal, being the quotes
        return t
    
    @_(r'\"[^\"]*\"')
    def STRING(self, t):
        t.value = t.value[1:-1] # Remove the first and last characters, which are always quotes
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
    data = """
            f1 (R[2 - 5])('s' 's') {}
    """
    lexer = DMDLexer()
    for tok in lexer.tokenize(data):
        print(tok)