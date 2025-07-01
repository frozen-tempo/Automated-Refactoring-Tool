import ast
from code_metrics.cls import Class

class HalsteadMetricsVisitor(ast.NodeVisitor):

    def __init__(self):
        self.operators = 0
        self.operands = 0
        self.unique_operators = set()
        self.unique_operands = set()
        self.location = 0
        self.functions = []

    def generic_visit(self, node: ast.AST):
        
        #print(self.unique_operators)
        super().generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += len(node.values)
        self.unique_operands.add(node.values)    

    def visit_BinOp(self, node: ast.BinOp):
        self.operators += 1
        self.operands += 2

        if isinstance(node.left, ast.Name):
            self.unique_operands.add(node.left.id)
        elif isinstance(node.right, ast.Name):
            self.unique_operands.add(node.right.id)

        if isinstance(node.left, ast.Constant):
            self.unique_operands.add(node.left.value)
        elif isinstance(node.right, ast.Constant):
            self.unique_operands.add(node.right.value)

        self.unique_operators.add(node.op.__class__.__name__)


    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += 1
        self.unique_operands.add(node.operand.value)

    def visit_AugAssign(self, node: ast.AugAssign):
        pass

    def visit_Compare(self, node: ast.Compare):
        pass

    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass
    