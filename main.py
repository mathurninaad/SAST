import ast
import re

class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.sast = []

    def check_hardcoded(self, target):
        name = target.id.lower()
        pattern = r"\b\w*(pass(word|wd)?|pwd|psswd)\w*\b"

        if re.search(pattern, name, re.IGNORECASE):
            self.sast.append((target.lineno, name))
            return True
        return False

    def visit_For(self, node):
        print(node.lineno)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            # Checking if the line has multiple assignments
            if isinstance(target, ast.Tuple):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.check_hardcoded(elt)
            # checking single line assignment
            elif isinstance(target, ast.Name):
                self.check_hardcoded(target)

        self.generic_visit(node)

    def printIssues(self):
        for issue in self.sast:
            print(f"Issue on line: {issue[0]} [Possibility of Hardcoded password]. variable Name: {issue[1]}")

if __name__ == '__main__':
    visitor = MyVisitor()
    with open('test.py') as code:
        code = code.read()
        tree = ast.parse(code)
        # print(ast.dump(tree, indent=4))
        visitor.visit(tree)
        visitor.printIssues()