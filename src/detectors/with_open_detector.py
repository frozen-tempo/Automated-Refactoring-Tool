import ast

class WithOpenDetector:

    def __init__(self):
        self.open_exists = False
        self.with_exists = False
        self.location = None

    def check(self, node: ast.FunctionDef, violations):

        if isinstance(node, ast.FunctionDef):
            self.location = node.lineno

            for ast_child_node in ast.walk(node):
                if isinstance(ast_child_node, ast.Name) and ast_child_node.id == 'open':
                    self.open_exists = True
                if isinstance(ast_child_node, ast.With):
                    self.with_exists= True

        if self.open_exists and not self.with_exists:
                violations.append({
                    "Line Number:" : self.location,
                    "Code Smell Type:" : "Using Open w/o With"
        })