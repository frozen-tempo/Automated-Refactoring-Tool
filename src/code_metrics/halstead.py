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
        
        super().generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += len(node.values)
        for operand in node.values:
            self.unique_operands.add(operand.id)

    def visit_BinOp(self, node: ast.BinOp):
        self.operators += 1
        self.operands += 2

        if isinstance(node.left, ast.Name):
            self.unique_operands.add(node.left.id)
        if isinstance(node.right, ast.Name):
            self.unique_operands.add(node.right.id)

        if isinstance(node.left, ast.Constant):
            self.unique_operands.add(node.left.value)
        if isinstance(node.right, ast.Constant):
            self.unique_operands.add(node.right.value)

        if isinstance(node.left, ast.BinOp):
            self.visit_BinOp(node.left)
        if isinstance(node.right, ast.BinOp):
            self.visit_BinOp(node.right)

        self.unique_operators.add(node.op.__class__.__name__)


    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += 1
        self.unique_operands.add(node.operand.value)

    def visit_AugAssign(self, node: ast.AugAssign):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += 1
        self.unique_operands.add(node.target.id)
        if isinstance(node.value, ast.Name):
            self.unique_operands.add(node.value.id)
        if isinstance(node.value, ast.Constant):
            self.unique_operands.add(node.value.value)
        if isinstance(node.value, ast.BinOp):
            self.visit_BinOp(node.value)


    def visit_Compare(self, node: ast.Compare):
        self.operators += len(node.ops)
        for op in node.ops:
            self.unique_operators.add(op.__class__.__name__)
        
        if isinstance(node.left, ast.Name):
            self.operands += 1
            self.unique_operands.add(node.left.id)
        if isinstance(node.right, ast.Name):
            self.operands += 1
            self.unique_operands.add(node.right.id)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass
    