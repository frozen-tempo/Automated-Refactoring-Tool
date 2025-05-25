import ast

class WildcardImportDetector:

    def __init__(self):
        self.location = None

    def check(self, node:ast.ImportFrom, violations):
        if isinstance(node, ast.ImportFrom):
            self.location = node.lineno
            for alias in node.names:
                if alias.name == "*":
                    violations.append({
                    "Line Number:" : self.location,
                    "Code Smell Type:" : "Wildcard Import"
                    })