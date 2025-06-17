import ast
class CodeMetricsVisitor(ast.NodeVisitor):
    
    def __init__(self):
        self.cyclomatic_complexity = 1
        self.halstead_vocab = 0
        self.halstead_length = 0
        self.halstead_volume = 0
        self.halstead_difficulty = 0
        self.halstead_effort = 0
        self.cognitive_complexity = 0
        self.maintainability_index = 0
        self.lines_of_code = 0

    def visit(self, node):
        print(f"Visiting: {node}")
        self.calculate_cyclomatic(node)
        self.generic_visit(node)

    def calculate_cyclomatic(self, node: ast.AST):
        self.decision_points = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.ExceptHandler, ast.Assert, ast.IfExp, ast.comprehension, ast.BoolOp)
        if isinstance(node, self.decision_points):
            self.cyclomatic_complexity += 1
        print(f"Cyclomatic Complexity: {self.cyclomatic_complexity}")
        

with open('src/code_smells.py', 'r') as f:
    source_code = f.read()

CodeMetricsVisitor().visit(ast.parse(source_code))
