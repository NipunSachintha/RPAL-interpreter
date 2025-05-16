from lexer import Lexer
from parser import Parser, TokenStorage, Tree

def parse_input(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    token_storage = TokenStorage.get_instance()
    token_storage.set_tokens(tokens)

    Parser.node_stack = []
    Parser.parse()

    return Tree.get_instance().ast_root
