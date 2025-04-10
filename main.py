import ast

class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_For(self, node):
        print(node.lineno)

