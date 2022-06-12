from rply import ParserGenerator
from ast_lan import Print, Number, Addition, Substraction, Multiplication, Division

class Parser():
    def __init__(self, module, builder, printf):
        self.module = module
        self.builder = builder
        self.printf = printf
        self.pg = ParserGenerator([
            'NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
            'SUM', 'SUB', 'MUL', 'DIV'
        ], precedence=[('left', ['SUM', 'SUB']), ('left', ['DIV', 'MUL'])])

    def parse(self):
        @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN')
        def program(p):
            return Print(self.builder, self.module, self.printf, p[2])
        
        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]

            if operator.gettokentype() == 'SUM':
                return Addition(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Substraction(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MUL':
                return Multiplication(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Division(self.builder, self.module, left, right)
    
        @self.pg.production('expression : expression expression SUM')
        @self.pg.production('expression : expression expression SUB')
        @self.pg.production('expression : expression expression MUL')
        @self.pg.production('expression : expression expression DIV') 
        def rpn_expression(p):
            left = p[0]
            right = p[1]
            operator = p[2]

            if operator.gettokentype() == 'SUM':
                return Addition(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Substraction(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MUL':
                return Multiplication(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Division(self.builder, self.module, left, right)
        
        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)
        
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)
    
    def get_parser(self):
        return self.pg.build()
