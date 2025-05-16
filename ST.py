def standardize(node):
    if not node or not node.children:
        return node

    node.children = [standardize(child) for child in node.children]

    label = node.label

    # Rule 1: let X = E in P  →  (gamma (lambda X P) E)
    if label == 'let':
        eq_node = node.children[0]
        P = node.children[1]
        
        if eq_node.label == '=' and len(eq_node.children) == 2:
            X = eq_node.children[0]
            E = eq_node.children[1]
            lambda_node = ASTNode('lambda', [X, P])
            return ASTNode('gamma', [lambda_node, E])
        else:
            raise Exception("Malformed 'let' expression")


    # Rule 2: where x = e1 and e2  →  (gamma (lambda x e2) e1)
    if label == 'where':
        # where -> gamma(lambda(X P), E)
        eq = node.children[1]  # x = e
        P = node.children[0]   # expression using x
        X = eq.children[0]     # variable x
        E = eq.children[1]     # expression e
        lambda_node = ASTNode('lambda', [X, P])
        return ASTNode('gamma', [lambda_node, E])

    # Rule 3: function_form x1 x2 ... xn = E
    # → x1 = lambda x2 ... xn . E
    if label == 'fcn_form':
        vars = node.children[:-1]
        expr = node.children[-1]
        for var in reversed(vars[1:]):
            expr = ASTNode('lambda', [var, expr])
        return ASTNode('=', [vars[0], expr])

    # Rule 4: lambda x1 x2 ... xn . E
    if label == 'lambda' and len(node.children) > 2:
        expr = node.children[-1]
        for var in reversed(node.children[:-1]):
            expr = ASTNode('lambda', [var, expr])
        return expr

    # Rule 5: within x1 = e1 and x2 = e2 → x2 = (gamma (lambda x1 e2) e1)
    if label == 'within':
        eq1 = node.children[0]
        eq2 = node.children[1]
        x1, e1 = eq1.children
        x2, e2 = eq2.children
        lambda_node = ASTNode('lambda', [x1, e2])
        gamma_node = ASTNode('gamma', [lambda_node, e1])
        return ASTNode('=', [x2, gamma_node])

    # Rule 6: and x1 = e1 , x2 = e2 , ... → = (x1 x2 ...) (e1 e2 ...)
    if label == 'and':
        vars = []
        exprs = []
        for child in node.children:
            if child.label == '=':
                vars.append(child.children[0])
                exprs.append(child.children[1])
        tuple1 = ASTNode(',', vars)
        tuple2 = ASTNode('tau', exprs)
        return ASTNode('=', [tuple1, tuple2])

    # Rule 7: rec x = e → x = (Y* (lambda x e))
    if label == 'rec':
        X = node.children[0]
        E = node.children[1]
        lambda_node = ASTNode('lambda', [X, E])
        ystar = ASTNode('Y*', [])
        return ASTNode('=', [X, ASTNode('gamma', [ystar, lambda_node])])

    # Rule 8: E1 @ N @ E2  →  gamma (gamma E1 N) E2

    if label == '@':
        E1 = node.children[0]
        N = node.children[1]
        E2=node.children[2]
        intermediate=ASTNode('gamma',[N,E1])
        return ASTNode('gamma', [intermediate, E2])
    

      
    value = getattr(node, 'value', None)
    return ASTNode(label, node.children, value=value)

    '''

    # Rule 10: not e → gamma not e
    if label == 'not':
        return ASTNode('gamma', [ASTNode('not', []), node.children[0]])

    # Rule 11: binary ops → gamma (gamma op e1) e2
    if label in ['+', '-', '*', '/', '**', 'gr', 'ge', 'ls', 'le', 'eq', 'ne', 'or', '&']:
        return ASTNode('gamma', [
            ASTNode('gamma', [ASTNode(label, []), node.children[0]]),
            node.children[1]
        ])
    
        
    # Rule 9: → e1 e2 e3 → gamma (gamma e1 e2) e3
    if len(node.children) > 2 and label not in {'tau', ',', 'lambda'}:
        new_node = ASTNode('gamma', [node.children[0], node.children[1]])
        for i in range(2, len(node.children)):
            new_node = ASTNode('gamma', [new_node, node.children[i]])
        return new_node

    # Rule 10: not e → gamma not e
    if label == 'not':
        return ASTNode('gamma', [ASTNode('not', []), node.children[0]])

    # Rule 11: binary ops → gamma (gamma op e1) e2
    if label in ['+', '-', '*', '/', '**', 'gr', 'ge', 'ls', 'le', 'eq', 'ne', 'or', '&']:
        return ASTNode('gamma', [
            ASTNode('gamma', [ASTNode(label, []), node.children[0]]),
            node.children[1]
        ])


    # Rule 12: | e1 e2 → gamma (gamma eta e1) e2
    if label == 'aug':
        return ASTNode('gamma', [
            ASTNode('gamma', [ASTNode('aug', []), node.children[0]]),
            node.children[1]
        ])

    # Rule 13: Tuples (tau)
    if label == 'tau' and len(node.children) > 1:
        return ASTNode(',', node.children)

    return node

    '''

class ASTNode:
    def __init__(self, label, children=None, value=None):
        self.label = label
        self.children = children if children else []
        self.value = value  # Token value like 'x', 5, etc.

    def __repr__(self, level=0):
        indent = '  ' * level
        val_str = f":{self.value}" if self.value is not None else ""
        res = f"{indent}{self.label}{val_str}\n"
        for child in self.children:
            res += child.__repr__(level + 1)
        return res
