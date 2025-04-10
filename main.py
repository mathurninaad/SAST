import ast

class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_For(self, node):
        print(node.lineno)
        self.generic_visit(node) # visit the children nodes of For


if __name__ == '__main__':
    visitor = MyVisitor()
    with open('test.py') as code:
        code = code.read()
        tree = ast.parse(code)
        visitor.visit(tree)