from lexer import Lexer
from parser import Parser
from code_gen import CodeGen

text_input = """
print(1 2 3 / +)
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()
module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

codegen.create_ir()
codegen.save_ir('output.ll')