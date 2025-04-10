import ast
import re

class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        # Problems in Python code
        self.sastP = []

        # unused variables and used variables
        self.unv = []
        self.uv = []



    def check_hardcoded(self, target):
        name = target.id.lower()
        pattern = r"\b\w*(pass(word|wd)?|pwd|psswd)\w*\b" # copied pattern from GPT

        if re.search(pattern, name, re.IGNORECASE):
            self.sastP.append((target.lineno, name))
            return True
        return False

    def visit_Assign(self, node):
        for target in node.targets:
            # multiple assignments
            if isinstance(target, ast.Tuple):
                for elt in target.elts:
                    self.unv.append((elt.id, elt.lineno))
                    if isinstance(elt, ast.Name):
                        self.check_hardcoded(elt)
            # checking single line assignment
            elif isinstance(target, ast.Name):
                self.unv.append((target.id, target.lineno))
                self.check_hardcoded(target)

        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.uv.append((node.id, node.lineno))
        self.generic_visit(node)

    def printIssues(self):
        for i in self.unv:
            found = False
            for j in self.uv:
                if j[0] == i[0]:
                    found =  True
            if found is False:
                print(f"Issue on line: {i[1]} [Unused variable]. variable name: {i[0]}")

        for issue in self.sastP:
            print(f"Issue on line: {issue[0]} [Possibility of Hardcoded password]. variable Name: {issue[1]}")

if __name__ == '__main__':
    visitor = MyVisitor()
    with open('test.py') as code:
        code = code.read()
        tree = ast.parse(code)
        print(ast.dump(tree, indent=4))
        visitor.visit(tree)
        visitor.printIssues()