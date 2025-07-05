import ast

class Function:

    def __init__(self):
        self.name = ""
        self.MLoC = 0 # Lines of code within a function/method (excluding comments and empty lines)
        self.complexity = 0 # Cyclomatic complexity for function/method
        self.NoP = 0 
        self.NoLV = 0
        self.branches = 0
        self.long_function = False
    
    def __str__(self):
        return f"Function(name={self.name}, MLoC={self.MLoC}, complexity={self.complexity}, NoP={self.NoP}, NoLV={self.NoLV}, branches={self.branches}, long_function={self.long_function})"

class LongFunctionDetector(ast.NodeVisitor):

    def __init__(self):
        self.functions = []

    def generic_visit(self, node: ast.AST):
        pass

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func = Function()
        func.name = node.name

        for child in node.body:
            if isinstance(child, ast.Name):
                func.NoLV += 1
            if isinstance(child, ast.If):
                func.branches += 1
            if isinstance(child, ast.Match):
                func.branches += len(child.cases)
            