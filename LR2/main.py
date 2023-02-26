import sys

class Lexer:
    OPERATORS = ['{', '}', '=', ';', '(', ')', '+', '-', '<', '>', '+=', '-=', '*=', '/=', '!=', '<=', '>=', '==', '*', '/', '%', ',', '<<']

    WORDS = ['if', 'else', 'do', 'while', 'for', 'int', 'float', 'string', 'break', 'return', 'continue', 'cout']

    VARS = []

    type = ''

    const = ''

    line = 1

    position = -1

    ch = ' '

    def error(self, msg, line, pos):
        print('Lexer error in line(', line,') and position(', pos, '): ', msg)
        sys.exit(1)

    def getc(self, file):
        self.ch = file.read(1)

    def next_tok(self, file):
        Lexer.const = ''
        self.value = None
        while True:
            if (len(self.ch) == 0):
                return
            if self.ch == '\n':
                Lexer.line = Lexer.line + 1
                Lexer.position = 0
                Lexer.type = ''
                self.getc(file)
            elif self.ch.isspace():
                self.getc(file)
                Lexer.position = Lexer.position + 1
            elif self.ch in Lexer.OPERATORS or self.ch == '!':
                ident = ''
                if self.ch == ';':
                    Lexer.type = ''
                if self.ch == '(' or self.ch =='{' or self.ch ==')' or self.ch =='}':
                    ident = self.ch
                    self.getc(file)
                    Lexer.position = Lexer.position + 1
                    return ident
                else:
                    while self.ch in Lexer.OPERATORS or self.ch == '!':
                        ident = ident + self.ch.lower()
                        self.getc(file)
                        Lexer.position = Lexer.position + 1
                    if ident in Lexer.OPERATORS and ident != '!':
                        return ident
                    else:
                        self.error('Unknown identifier: ' + ident, Lexer.line, Lexer.position)
            elif self.ch.isdigit() or self.ch == '.':
                intval = 0
                counter = 0
                numcounter = 0
                while self.ch.isdigit() or self.ch == '.':
                    if self.ch.isdigit():
                        intval = intval * 10 + int(self.ch)
                        if counter == 1:
                            numcounter = numcounter + 1
                    else:
                        if self.ch == '.':
                            counter = counter + 1
                    if counter == 2:
                        self.error('incorrect value', Lexer.line, Lexer.position)
                    self.getc(file)
                    Lexer.position = Lexer.position + 1
                    if self.ch.isalpha():
                        self.error('user defined literal operator not found', Lexer.line, Lexer.position)
                if numcounter !=  0:
                    intval = intval / (10 ** numcounter)
                self.value = intval
                return self.value
            elif self.ch.isalpha():
                ident = ''
                while self.ch.isalpha() or self.ch.isdigit():
                    ident = ident + self.ch.lower()
                    self.getc(file)
                    Lexer.position = Lexer.position + 1
                if ident == 'int' or ident == 'float' or ident == 'string':
                    Lexer.type = ident
                    return ident
                elif ident in Lexer.WORDS:
                    return ident
                elif ident in Lexer.VARS:
                    return ident
                elif Lexer.type != '' and ident not in Lexer.VARS:
                    Lexer.VARS.append(ident)
                    return ident
                else:
                    self.error('Unknown identifier: ' + ident, Lexer.line, Lexer.position)
            elif self.ch == '"':
                ident = ''
                self.getc(file)
                Lexer.position = Lexer.position + 1
                while self.ch != '"':
                    if len(self.ch) == 0:
                        self.error('Missing closing quote', Lexer.line, Lexer.position)
                    ident = ident + self.ch
                    self.getc(file)
                    Lexer.position = Lexer.position + 1
                Lexer.const = ident
                self.getc(file)
                Lexer.position = Lexer.position + 1
                return ident
            else:
                self.error('Unexpected symbol: ' + self.ch, Lexer.line, Lexer.position)

l = Lexer()
var = []
kw = []
oper = []
const = []
tables = {'identifiers': var, 'key words': kw, 'operators': oper, 'constants': const}
f = open("C:\\MTRan\LR2\Code.txt", "r")
while(len(l.ch) != 0):
    temp = l.next_tok(f)
    if temp in l.OPERATORS:
        tables['operators'].append(temp)
    else:
        if temp in l.WORDS:
            tables['key words'].append(temp)
        else:
            if isinstance(temp, str) and temp != l.const:
                tables['identifiers'].append(temp)
            elif temp != None:
                tables['constants'].append(temp)
l.VARS.clear()
print("KEYWORDS")
print(tables['key words'])
print("IDENTIFIERS")
print(tables['identifiers'])
print("OPERATORS")
print(tables['operators'])
print("CONSTANTS")
print(tables['constants'])