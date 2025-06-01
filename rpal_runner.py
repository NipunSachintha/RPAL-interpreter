# rpal_runner.py

from lexer import Lexer
from ST import standardize
from parser import Parser
from parser import TokenStorage, Tree
from CSE.cse_machine import CSEMachine 
from CSE.cse_factory import CSEMachineFactory


# this should be replaced with test_standardizer.py print_ast function logic


def print_ast(node, dots=0):
    if not node:
        return
    prefix = "." * dots
    if hasattr(node, 'value') and node.value in {"nil", "true", "false", "dummy"}:
        #print(f"{prefix}<nil>")
        print(f"{prefix}<{node.value}>")
    
    elif hasattr(node, 'value') and node.value is not None:
        print(f"{prefix}<{node.label}:{node.value}>")
    else:
        print(f"{prefix}{node.label}")
    for child in node.children:
        print_ast(child, dots + 1)


def run_pipeline(code):
    # 1. Lexical Analysis
    print("=== LEXER ===")
    lexer= Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

    # 2. Parsing to AST
    print("\n=== PARSER (AST) ===")
# Set up the token storage
    token_storage = TokenStorage.get_instance()
    token_storage.set_tokens(tokens)
            
    # Reset the parser state
    Parser.node_stack = []
            
    # Parse the program
    Parser.parse()
            
    # Get the AST
    ast = Tree.get_instance().ast_root
            
    # Print the AST structure
    print("\nAST Structure:")
    print_ast(ast)   
    

    # 3. Standardizing AST
    print("\n=== STANDARDIZED TREE ===")
    st = standardize(ast)
    print_ast(st)


    
    # Wrap it
    #wrapped_ast = ASTWrapper(st)

    # 4. Executing with CSE Machine
    print("\n=== CSE MACHINE OUTPUT ===")
    factory = CSEMachineFactory()
    cse = factory.get_cse_machine(st)
    result = cse.get_answer()
    if result is not None:
        print(result)

    



if __name__ == "__main__":
    # Sample RPAL code input
    rpal_code = """
    let x = 5 in
        x + 2
    """
    
    run_pipeline(rpal_code)
