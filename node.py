class Node:
    def __init__(self, value):
        self.level = 0
        self.value = value
        self.children = []  
        

# Recursively traverse each child nodes
def preorder_traversal(root):
    if root is None:
        return

    print("." * root.level + root.value)
    
    for child in root.children:
        child.level = root.level + 1
        preorder_traversal(child)  