from enum import Enum
from typing import List, Optional, Union

keywords = [
    "let", "in", "fn", "where", "rec", "and", "aug","within", "eq","ls"
]

class TokenType(str,Enum):
    """Enum representing the types of tokens in the RPAL language."""
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    #KEYWORD = "KEYWORD"
    END_OF_FILE = "EOF"
    #PUNCTUATION = "PUNCTUATION"


class Token:
    """Class representing a token in the RPAL language."""
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value


class TreeNode:
    """Base class for nodes in the Abstract Syntax Tree."""
    def __init__(self, label: str):
        self.label = label
        self.children = []

    def append_child(self, child):
        """Add a child node to this node."""
        self.children.append(child)

    def reverse_children_order(self):
        """Reverse the order of children."""
        self.children.reverse()


class LeafNode(TreeNode):
    """Class representing a leaf node in the Abstract Syntax Tree."""
    def __init__(self, label: str, value: str = ""):
        super().__init__(label)
        self.value = value


class InternalNode(TreeNode):
    """Class representing an internal node in the Abstract Syntax Tree."""
    pass


class Lexer:
    """Simple lexer class for demonstration purposes."""
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        """Tokenize the source code. Simplified for this example."""
        # This is a placeholder implementation
        # A real implementation would scan the source and produce tokens
        pass


class TokenStorage:
    """Singleton class for storing and accessing tokens."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TokenStorage()
        return cls._instance

    def __init__(self):
        self.tokens = []
        self.position = 0

    def set_tokens(self, tokens: List[Token]):
        """Set the tokens list."""
        self.tokens = tokens
        self.position = 0

    def top(self) -> Token:
        """Return the current token without consuming it."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token(TokenType.END_OF_FILE, "")

    def pop(self) -> Token:
        """Return the current token and advance to the next one."""
        token = self.top()
        self.position += 1
        return token


class Tree:
    """Singleton class representing the Abstract Syntax Tree."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Tree()
        return cls._instance

    def __init__(self):
        self.ast_root = None

    def set_ast_root(self, root: TreeNode):
        """Set the root of the AST."""
        self.ast_root = root


class Parser:
    """The Parser class is responsible for parsing a sequence of tokens and constructing the AST."""
    node_stack = []

    @staticmethod
    def parse():
        """Parse the input tokens and construct the AST."""
        token_storage = TokenStorage.get_instance()
        token = token_storage.top()

        # Check if the input token is the end of file token
        if token.type == TokenType.END_OF_FILE:
            return  # No further parsing required
        else:
            E()  # Start parsing the expression

            # Check if the next token is the end of file token
            if token_storage.top().type == TokenType.END_OF_FILE:
                # Set the root of the AST to the last node in the node_stack
                Tree.get_instance().set_ast_root(Parser.node_stack[-1])
                return  # Parsing completed
            else:
                raise SyntaxError("End of file expected")


def build_tree(label: str, num: int, is_leaf: bool, node_value: str = ""):
    """
    Construct a new TreeNode with the specified label, number of children, leaf status, and node_value.
    Add the constructed node to the node_stack.
    """
    if is_leaf:
        node = LeafNode(label, node_value)
    else:
        node = InternalNode(label)

    # Add the children from the node_stack to the newly created node
    for _ in range(num):
        node.append_child(Parser.node_stack.pop())

    # Reverse the order of the children
    node.reverse_children_order()

    # Push the constructed node onto the node_stack
    Parser.node_stack.append(node)


def E():
    """
    Parse the expression starting with E.
    Handles the grammar rule E -> "let" D "in" E | "fn" Vb+  "." E | Ew.
    """
    token_storage = TokenStorage.get_instance()

    # Check if the current token is "let"
    if token_storage.top().value == "let":
        token_storage.pop()
        D()

        # Check if the next token is "in"
        if token_storage.top().value == "in":
            token_storage.pop()
            E()
        else:
            raise SyntaxError("'in' expected")

        # Build the "let" node with 2 children
        build_tree("let", 2, False)
    # Check if the current token is "fn"
    elif token_storage.top().value == "fn":
        token_storage.pop()
        n = 0

        # Process identifiers until a non-identifier token is encountered
        while token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
            Vb()
            n += 1

        if n == 0:
            raise SyntaxError("At least one identifier expected")

        # Check if the next token is "."
        if token_storage.top().value == ".":
            token_storage.pop()
            E()
        else:
            raise SyntaxError("'.' expected")

        # Build the "lambda" node with n+1 children
        build_tree("lambda", n + 1, False)
    else:
        Ew()


def Ew():
    """
    Parse the expression starting with Ew.
    Handles the grammar rule Ew -> T [ "where" Dr ].
    """
    token_storage = TokenStorage.get_instance()
    T()

    # Check if the next token is "where"
    if token_storage.top().value == "where":
        token_storage.pop()
        Dr()
        build_tree("where", 2, False)


def T():
    """
    Parse the expression starting with T.
    Handles the grammar rule T -> Ta { "," Ta }.
    """
    token_storage = TokenStorage.get_instance()
    Ta()
    n = 0

    # Process additional T expressions separated by commas
    while token_storage.top().value == ",":
        token_storage.pop()
        Ta()
        n += 1

    if n > 0:
        build_tree("tau", n + 1, False)


def Ta():
    """
    Parse the expression starting with Ta.
    Handles the grammar rule Ta -> Tc { "aug" Tc }.
    """
    token_storage = TokenStorage.get_instance()
    Tc()

    # Process additional Tc expressions separated by "aug" keyword
    while token_storage.top().value == "aug":
        token_storage.pop()
        Tc()
        build_tree("aug", 2, False)


def Tc():
    """
    Parse the expression starting with Tc.
    Handles the grammar rule Tc -> B [ "->" Tc [ "|" Tc ] ].
    """
    token_storage = TokenStorage.get_instance()
    B()

    # Check if the next token is "->"
    if token_storage.top().value == "->":
        token_storage.pop()
        Tc()

        # Check if the next token is "|"
        if token_storage.top().value == "|":
            token_storage.pop()
            Tc()
            build_tree("->", 3, False)
        else:
            raise SyntaxError("'|' expected")


def B():
    """
    Parse the expression starting with B.
    Handles the grammar rule B -> Bt { "or" Bt }.
    """
    token_storage = TokenStorage.get_instance()
    Bt()

    # Process additional Bt expressions separated by "or" keyword
    while token_storage.top().value == "or":
        token_storage.pop()
        Bt()
        build_tree("or", 2, False)


def Bt():
    """
    Parse the expression starting with Bt.
    Handles the grammar rule Bt -> Bs { "&" Bs }.
    """
    token_storage = TokenStorage.get_instance()
    Bs()

    # Process additional Bs expressions separated by "&" keyword
    while token_storage.top().value == "&":
        token_storage.pop()
        Bs()
        build_tree("&", 2, False)


def Bs():
    """
    Parse the expression starting with Bs.
    Handles the grammar rule Bs -> "not" Bp | Bp.
    """
    token_storage = TokenStorage.get_instance()
    if token_storage.top().value == "not":
        token_storage.pop()
        Bp()
        build_tree("not", 1, False)
    else:
        Bp()


def Bp():
    """
    Parse the expression starting with Bp.
    Handles the grammar rule Bp -> A { comparison_operator A }.
    """
    token_storage = TokenStorage.get_instance()
    A()

    # Check for comparison operators
    if token_storage.top().value in ["gr", ">"]:
        token_storage.pop()
        A()
        build_tree("gr", 2, False)
    elif token_storage.top().value in ["ge", ">="]:
        token_storage.pop()
        A()
        build_tree("ge", 2, False)
    elif token_storage.top().value in ["ls", "<"]:
        token_storage.pop()
        A()
        build_tree("ls", 2, False)
    elif token_storage.top().value in ["le", "<="]:
        token_storage.pop()
        A()
        build_tree("le", 2, False)
    elif token_storage.top().value in ["eq", "="]:
        token_storage.pop()
        A()
        build_tree("eq", 2, False)
    elif token_storage.top().value in ["ne", "!="]:
        token_storage.pop()
        A()
        build_tree("ne", 2, False)


def A():
    """
    Parse the expression starting with A.
    Handles the grammar rule A -> + At | - At | At { + At | - At }.
    """
    token_storage = TokenStorage.get_instance()

    # Check for unary plus operator
    if token_storage.top().value == "+":
        token_storage.pop()
        At()
    # Check for unary minus operator
    elif token_storage.top().value == "-":
        token_storage.pop()
        At()
        build_tree("neg", 1, False)
    else:
        At()

    # Check for addition and subtraction operators
    while token_storage.top().value in ["+", "-"]:
        if token_storage.top().value == "+":
            token_storage.pop()
            At()
            build_tree("+", 2, False)
        elif token_storage.top().value == "-":
            token_storage.pop()
            At()
            build_tree("-", 2, False)


def At():
    """
    Parse the expression starting with At.
    Handles the grammar rule At -> Af { * Af | / Af }.
    """
    token_storage = TokenStorage.get_instance()
    Af()

    # Check for multiplication and division operators
    while token_storage.top().value in ["*", "/"]:
        if token_storage.top().value == "*":
            token_storage.pop()
            Af()
            build_tree("*", 2, False)
        elif token_storage.top().value == "/":
            token_storage.pop()
            Af()
            build_tree("/", 2, False)


def Af():
    """
    Parse the expression starting with Af.
    Handles the grammar rule Af -> Ap { ** Ap }.
    """
    token_storage = TokenStorage.get_instance()
    Ap()

    # Check for exponentiation operator
    while token_storage.top().value == "**":
        token_storage.pop()
        Ap()
        build_tree("**", 2, False)


def Ap():
    """
    Parse the expression starting with Ap.
    Handles the grammar rule Ap -> R { @ identifier R }.
    """
    token_storage = TokenStorage.get_instance()
    R()

    # Check for function application operator
    while token_storage.top().value == "@":
        token_storage.pop()

        # Check for identifier token
        if token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
            token = token_storage.pop()
            build_tree("identifier", 0, True, token.value)
        else:
            raise SyntaxError("Identifier expected")

        R()
        build_tree("@", 3, False)


def R():
    """
    Parse the expression starting with R.
    Handles the grammar rule R -> Rn { Rn }.
    """
    token_storage = TokenStorage.get_instance()
    Rn()

    top = token_storage.top()
    valid_types = [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING]
    valid_values = ["true", "false", "nil", "(", "dummy"]
    
    while (top.type in valid_types or top.value in valid_values) and top.value not in keywords:
        Rn()
        top = token_storage.top()
        build_tree("gamma", 2, False)


def Rn():
    """
    Parse the expression starting with Rn.
    Handles the grammar rule Rn -> identifier | integer | string | true | false | nil | ( E ) | dummy.
    """
    token_storage = TokenStorage.get_instance()
    top = token_storage.top()

    if top.type == TokenType.IDENTIFIER and top.value not in keywords:
        # Parse Identifier
        token = token_storage.pop()
        build_tree("identifier", 0, True, token.value)
    elif top.type == TokenType.INTEGER:
        # Parse Integer
        token = token_storage.pop()
        build_tree("integer", 0, True, token.value)
    elif top.type == TokenType.STRING:
        # Parse String
        token = token_storage.pop()
        build_tree("string", 0, True, token.value)
    elif top.value == "true":
        # Parse true
        token_storage.pop()
        build_tree("true", 0, True)
    elif top.value == "false":
        # Parse false
        token_storage.pop()
        build_tree("false", 0, True)
    elif top.value == "nil":
        # Parse nil
        token_storage.pop()
        build_tree("nil", 0, True)
    elif top.value == "(":
        token_storage.pop()
        E()
        if token_storage.top().value == ")":
            token_storage.pop()
        else:
            raise SyntaxError("')' expected")
    elif top.value == "dummy":
        # Parse dummy
        token_storage.pop()
        build_tree("dummy", 0, True)
    else:
        raise SyntaxError(f"Identifier, Integer, String, 'true', 'false', 'nil', '(', 'dummy' expected, got: {top.value}")


def D():
    """
    Parse the expression starting with D.
    Handles the grammar rule D -> Da [ within D ].
    """
    token_storage = TokenStorage.get_instance()
    Da()

    while token_storage.top().value == "within":
        token_storage.pop()
        D()
        build_tree("within", 2, False)


def Da():
    """
    Parse the expression starting with Da.
    Handles the grammar rule Da -> Dr { and Dr }.
    """
    token_storage = TokenStorage.get_instance()
    Dr()
    n = 0

    while token_storage.top().value == "and":
        token_storage.pop()
        Dr()
        n += 1
        
    if n > 0:
        build_tree("and", n + 1, False)


def Dr():
    """
    Parse the expression starting with Dr.
    Handles the grammar rule Dr -> rec Db | Db.
    """
    token_storage = TokenStorage.get_instance()

    if token_storage.top().value == "rec":
        token_storage.pop()
        Db()
        build_tree("rec", 1, False)
    else:
        Db()


def Db():
    """
    Parse the expression starting with Db.
    Handles the grammar rule Db -> ( D ) | identifier Vl = E | Vb { , Vb } = E | epsilon.
    """
    token_storage = TokenStorage.get_instance()

    if token_storage.top().value == "(":
        token_storage.pop()
        D()

        if token_storage.top().value == ")":
            token_storage.pop()
        else:
            raise SyntaxError("')' expected")
    elif token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
        # Parse Identifier
        token = token_storage.pop()
        build_tree("identifier", 0, True, token.value)

        if token_storage.top().value == ",":
            token_storage.pop()
            Vl()

            if token_storage.top().value == "=":
                token_storage.pop()
                E()
                build_tree("=", 2, False)
            else:
                raise SyntaxError("'=' expected")
        else:
            n = 0

            while token_storage.top().value != "=" and token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
                Vb()
                n += 1

            if token_storage.top().value == "(":
                Vb()
                n += 1

            if n == 0 and token_storage.top().value == "=":
                token_storage.pop()
                E()
                build_tree("=", 2, False)
            elif n != 0 and token_storage.top().value == "=":
                token_storage.pop()
                E()
                build_tree("fcn_form", n + 2, False)
            else:
                raise SyntaxError("'=' expected")
    else:
        raise SyntaxError("'(' or Identifier expected")


def Vb():
    """
    Parse the expression starting with Vb.
    Handles the grammar rule Vb -> identifier | ( ) | ( identifier Vl ).
    """
    token_storage = TokenStorage.get_instance()

    if token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
        # Parse Identifier
        token = token_storage.pop()
        build_tree("identifier", 0, True, token.value)
    elif token_storage.top().value == "(":
        token_storage.pop()

        if token_storage.top().value == ")":
            token_storage.pop()
            build_tree("()", 0, True)
        elif token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
            # Parse Identifier
            token = token_storage.pop()
            build_tree("identifier", 0, True, token.value)

            if token_storage.top().value == ",":
                token_storage.pop()
                Vl()

            if token_storage.top().value == ")":
                token_storage.pop()
            else:
                raise SyntaxError("')' expected")
        else:
            raise SyntaxError("Identifier or ')' expected")
    else:
        raise SyntaxError("Identifier or '(' expected")


def Vl():
    """
    Parse the expression starting with Vl.
    Handles the grammar rule Vl -> identifier { , identifier }.
    """
    token_storage = TokenStorage.get_instance()

    if token_storage.top().type == TokenType.IDENTIFIER and token_storage.top().value not in keywords:
        # Parse Identifier
        token = token_storage.pop()
        build_tree("identifier", 0, True, token.value)

        n = 2
        while token_storage.top().value == ",":
            token_storage.pop()
            token = token_storage.pop()
            build_tree("identifier", 0, True, token.value)
            n += 1

        build_tree(",", n, False)
    else:
        raise SyntaxError("Identifier expected")


# Example usage function (not part of the parser itself)
def parse_rpal_program(source_code: str):
    """Parse an RPAL program and return the AST."""
    # Create a lexer and tokenize the source code
    lexer = Lexer(source_code)
    
    # Set the tokens in TokenStorage
    token_storage = TokenStorage.get_instance()
    token_storage.set_tokens(lexer.tokens)
    
    # Parse the tokens and build the AST
    Parser.parse()
    
    # Return the root of the AST
    return Tree.get_instance().ast_root