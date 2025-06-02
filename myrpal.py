"""
RPAL Interpreter Main File
Usage: python myrpal.py [-l] [-ast] [-st] filename
"""

import sys
from lexer import Lexer
from ST import standardize
from parser import Parser, TokenStorage, Tree
from CSE.cse_factory import CSEMachineFactory
from csemachine import *


def print_ast(node, dots=0):
    """Print AST in the required format"""
    if not node:
        return
    prefix = "." * dots
    if hasattr(node, 'value') and node.value in {"nil", "true", "false", "dummy"}:
        print(f"{prefix}<{node.value}>")
    elif hasattr(node, 'value') and node.value is not None:
        print(f"{prefix}<{node.label}:{node.value}>")
    else:
        print(f"{prefix}{node.label}")
    for child in node.children:
        print_ast(child, dots + 1)

def parse_file(filename):
    """Parse a file and return the AST"""
    try:
        with open(filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
    
    # Lexical Analysis
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Set up the token storage
    token_storage = TokenStorage.get_instance()
    token_storage.set_tokens(tokens)
    
    # Reset the parser state
    Parser.node_stack = []
    
    # Parse the program
    Parser.parse()
    
    # Get the AST
    ast = Tree.get_instance().ast_root
    return ast

def print_lexer_output(filename):
    """Print lexer output (-l flag)"""
    try:
        with open(filename, 'r') as file:
            code = file.read()
            print(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

def print_ast_output(filename):
    """Print AST output (-ast flag)"""
    ast = parse_file(filename)
    print_ast(ast)

def print_st_output(filename):
    """Print standardized tree output (-st flag)"""
    ast = parse_file(filename)
    st = standardize(ast)
    print_ast(st)

def execute_program(filename):
    """Execute the program and print result"""
    try:
        ast = parse_file(filename)
        st = standardize(ast)
        result  = get_result(filename)
        
        
        #Create CSE Machine and execute
        #factory = CSEMachineFactory()
        #cse_machine = factory.get_cse_machine(st)
        #result = cse_machine.get_answer()
        if result is not None:
            print(result)
        
    except Exception as e:
        print(f"Error executing program: {e}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments"""
    arguments = sys.argv
    
    if len(arguments) < 2:
        print("Wrong command. Make sure the command is in the following format.")
        print("python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)
    
    # Case 1: Only filename provided (execute program)
    if len(arguments) == 2:
        filename = arguments[1]
        execute_program(filename)
        return
    
    # Case 2: Switches provided
    switches = arguments[1:-1]
    filename = arguments[-1]
    
    # Validate switches
    valid_switches = {"-l", "-ast", "-st"}
    for switch in switches:
        if switch not in valid_switches:
            print("Wrong command. Make sure the command is in the following format.")
            print("python ./myrpal.py [-l] [-ast] [-st] filename")
            sys.exit(1)
    
    # Handle switches in order
    output_printed = False
    
    if "-l" in switches:
        print_lexer_output(filename)
        output_printed = True
        if len(switches) > 1:
            print()  # Add newline between outputs
    
    if "-ast" in switches:
        print_ast_output(filename)
        output_printed = True
        if "-st" in switches:
            print()  # Add newline before ST output
    
    elif "-st" in switches:
        print_st_output(filename)
        output_printed = True
    
    # If any switch was used, don't execute the program
    if not output_printed:
        print("Wrong command. Make sure the command is in the following format.")
        print("python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)

if __name__ == "__main__":
    main()