import ast
import re

class SASTDetector(ast.NodeVisitor):
    def __init__(self):
        # hardcoded passwords
        self.sastP = []

        # unused variables and used variables
        self.unv = []
        self.uv = []

        # dangerous os functions
        self.dangerous_func = []

    def check_hardcoded(self, target):
        name = target.id.lower()
        pattern = r"\b\w*(pass(word|wd)?|pwd|psswd)\w*\b" # copied pattern from GPT

        if re.search(pattern, name, re.IGNORECASE):
            self.sastP.append((target.lineno, name))
            return True
        return False

    def get_func_name(self, node):
        pass

    def visit_Call(self, node):
        func_name = self.get_func_name(node.func)
        danger_keywords = {"system", "popen", "call", "Popen", "eval", "exec", "compile"}
        if any(keyword in func_name for keyword in danger_keywords):
            self.dangerous_func.append((node.lineno, func_name))

        self.generic_visit(node)

    def get_func_name(self, func):
        if isinstance(func, ast.Attribute): # means that we are calling the function of an object
            parts = []
            while isinstance(func, ast.Attribute):
                parts.append(func.attr)
                func = func.value
            if isinstance(func, ast.Name): # we are calling the function
                parts.append(func.id)
            return ".".join(reversed(parts))
        elif isinstance(func, ast.Name):
            return func.id
        return ""

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
        for i in self.dangerous_func:
            print(f"Issue on line: {i[0]} [Dangerous Function]. Function name: {i[1]}")
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
    visitor = SASTDetector()
    with open('test.py') as code:
        code = code.read()
        tree = ast.parse(code)
        print(ast.dump(tree, indent=4))
        visitor.visit(tree)
        visitor.printIssues()