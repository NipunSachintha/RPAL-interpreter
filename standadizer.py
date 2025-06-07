# Compatible Node class for the standardizer
from parser import TokenStorage, Parser, Tree  # Import the parser components

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

# Adapter function to convert parser's TreeNode to standardizer's Node
def convert_tree_to_node(tree_node):
    """Convert TreeNode/LeafNode from parser to Node in standardizer for ease of use"""
    if tree_node is None:
        return None
    
    # Get the label as the value
    if hasattr(tree_node, 'label'):
        value = tree_node.label
        #print("Converting TreeNode with label:", value)
    else:
        value = str(tree_node)
    

    if hasattr(tree_node, 'value') and tree_node.value is not None:
    # Special literals
        if tree_node.value in ["true", "false", "nil", "dummy"]:
            value = f"<{tree_node.value}>"
        elif value == "ID":
            value = f"<ID:{tree_node.value}>"
        elif value == "INT":
            value = f"<INT:{tree_node.value}>"
        elif value == "STR":
            value = f"<STR:{tree_node.value}>"
    
    # Convert children recursively
    converted_children = []
    if hasattr(tree_node, 'children'):
        for child in tree_node.children:
            converted_child = convert_tree_to_node(child)
            if converted_child:
                converted_children.append(converted_child)
    
    return Node(value, converted_children)

# Updated standardizer function to work with the second parser
def standardize(tree_root):
    """
    Standardize AST from the second parser implementation
    """
    # Convert the parser's tree structure to the standardizer's expected format
    node_root = convert_tree_to_node(tree_root)
    #print("Converted Node Root:", node_root.value)
    
    # Apply the original standardization logic
    standardized_node = make_standardized_tree(node_root)
    
    return standardized_node

# The original make_standardized_tree function (from paste.txt)
def make_standardized_tree(root):
    if root is None:
        return None
        
    # Recursively standardize children first
    for child in root.children:
        make_standardized_tree(child)

    if root.value == "let" and len(root.children) > 0 and root.children[0].value == "=":
        child_0 = root.children[0]
        child_1 = root.children[1]

        root.children[1] = child_0.children[1]
        root.children[0].children[1] = child_1
        root.children[0].value = "lambda"
        root.value = "gamma"

    elif root.value == "where" and len(root.children) > 1 and root.children[1].value == "=":
        child_0 = root.children[0] 
        child_1 = root.children[1] 

        root.children[0] = child_1.children[1]
        root.children[1].children[1] = child_0
        root.children[1].value = "lambda"
        root.children[0], root.children[1] = root.children[1], root.children[0]
        root.value = "gamma"

    elif root.value == "fcn_form":  # Note: parser uses "fcn_form", not "function_form"
        
        if len(root.children) > 1:
            expression = root.children.pop()

            current_node = root
            for i in range(len(root.children) - 1):
                lambda_node = Node("lambda")
                child = root.children.pop(1)
                lambda_node.children.append(child)
                current_node.children.append(lambda_node)
                current_node = lambda_node

            current_node.children.append(expression)
            root.value = "="

    elif root.value == "gamma" and len(root.children) > 2:
        '''Handle multi-argument gamma expressions'''
        expression = root.children.pop()

        current_node = root
        for i in range(len(root.children) - 1):
            gamma_node = Node("gamma")
            child = root.children.pop(1)
            gamma_node.children.append(child)
            current_node.children.append(gamma_node)
            current_node = gamma_node

        current_node.children.append(expression)

    elif root.value == "within" and len(root.children) >= 2 and \
         root.children[0].value == "=" and root.children[1].value == "=":
        
        child_0 = root.children[1].children[0]
        child_1 = Node("gamma")

        child_1.children.append(Node("lambda"))
        child_1.children.append(root.children[0].children[1])
        child_1.children[0].children.append(root.children[0].children[0])
        child_1.children[0].children.append(root.children[1].children[1])

        root.children[0] = child_0
        root.children[1] = child_1
        root.value = "="

    elif root.value == "@" and len(root.children) >= 3:
        expression = root.children.pop(0)
        identifier = root.children[0]

        gamma_node = Node("gamma")
        gamma_node.children.append(identifier)
        gamma_node.children.append(expression)

        root.children[0] = gamma_node
        root.value = "gamma"

    elif root.value == "and":
        child_0 = Node(",")
        child_1 = Node("tau")

        for child in root.children:
            if len(child.children) >= 2:
                child_0.children.append(child.children[0])
                child_1.children.append(child.children[1])

        root.children.clear()
        root.children.append(child_0)
        root.children.append(child_1)
        root.value = "="

    elif root.value == "rec":
        if len(root.children) > 0:
            temp = root.children[0]  # This should be the = node
            if temp.value == "=" and len(temp.children) >= 2:
                x_node = temp.children[0]
                e_node = temp.children[1]
                
                lambda_node = Node("lambda")
                lambda_node.children.append(x_node)
                lambda_node.children.append(e_node)

                gamma_node = Node("gamma")
                gamma_node.children.append(Node("<Y*>"))
                gamma_node.children.append(lambda_node)

                root.children.clear()
                root.children.append(x_node)
                root.children.append(gamma_node)
                root.value = "="

    return root

# Function to print the tree for debugging
def print_tree(node, dots=0):
    """Print the tree structure for debugging"""
    if node is None:
        return
    
    print("." * dots + str(node.value))
    for child in node.children:
        print_tree(child, dots + 1)

# Example usage function
def parse_and_standardize(source_tokens):
    
    # Set up the token storage
    token_storage = TokenStorage.get_instance()
    token_storage.set_tokens(source_tokens)
    
    # Parse the tokens
    Parser.parse()
    
    # Get the AST root
    ast_root = Tree.get_instance().ast_root
    
    # Standardize the AST
    standardized_ast = standardize(ast_root)
    
    return standardized_ast