import ast
from code_metrics.func import Function
from code_metrics.cls import Class

class HalsteadMetricsVisitor(ast.NodeVisitor):

    def __init__(self):
        self.operators = 0
        self.operands = 0
        self.unique_operators = set()
        self.unique_operands = set()
        self.functions = []

    def generic_visit(self, node: ast.AST):

        if node.__class__.__name__ in [ 'If', 'IfExp', 'While', 'For', 'With', 'Try', 'TryExcept']:
            self.operators += 1
            self.unique_operators.add(node.__class__.__name__)
        
        super().generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += len(node.values)
        for operand in node.values:
            self.unique_operands.add(operand.id)

        self.generic_visit(node)

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

        self.generic_visit(node)


    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.operators += 1
        self.unique_operators.add(node.op.__class__.__name__)
        self.operands += 1
        self.unique_operands.add(node.operand.value)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # LHS of assignment
        self.operators += 1
        self.unique_operators.add(node.__class__.__name__)
        if isinstance(node.targets[0], ast.Name):
            self.operands += 1
            self.unique_operands.add(node.targets[0].id)
        if isinstance(node.targets, ast.Tuple):
            for target in node.targets.elts:
                if isinstance(target, ast.Name):
                    self.operands += 1
                    self.unique_operands.add(target.id)
                if isinstance(target, ast.Constant):
                    self.operands += 1
                    self.unique_operands.add(target.value)
        #RHS of assignment
        if isinstance(node.value, ast.Name):
            self.operands += 1
            self.unique_operands.add(node.value.id)
        if isinstance(node.value, ast.Constant):
                self.operands += 1
                self.unique_operands.add(node.value.value)
        if isinstance(node.value, ast.Tuple):
            for val in node.value.elts:
                if isinstance(val, ast.Name):
                    self.operands += 1
                    self.unique_operands.add(val.id)
                if isinstance(val, ast.Constant):
                    self.operands += 1
                    self.unique_operands.add(val.value)

        self.generic_visit(node)
        

    def visit_AugAssign(self, node: ast.AugAssign):
        # Augmented assignment (e.g., +=, -=, etc.)
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

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        # Comparison operations (e.g., <, >, ==, etc.)
        self.operators += len(node.ops)
        for op in node.ops:
            self.unique_operators.add(op.__class__.__name__)
        self.operands += len(node.comparators) + 1
        if isinstance(node.left, ast.Name):
            self.unique_operands.add(node.left.id)
        if isinstance(node.left, ast.Constant):
            self.unique_operands.add(node.left.value)
        for comp in node.comparators:
            if isinstance(comp, ast.Name):
                self.unique_operands.add(comp.id)
            if isinstance(comp, ast.Constant):
                self.unique_operands.add(comp.value)
        
    def visit_Call(self, node: ast.Call):
        self.operators += 1
        self.unique_operators.add(node.func.id)
        self.operands += len(node.args)
        for arg in node.args:
            if isinstance(arg, ast.Name):
                self.unique_operands.add(arg.id)
            if isinstance(arg, ast.Constant):
                self.unique_operands.add(arg.value)

        
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass
    