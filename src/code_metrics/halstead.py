import ast
import math

class HalsteadMetricsVisitor(ast.NodeVisitor):

    def __init__(self):
        self.operators = 0
        self.operands = 0
        self.unique_operators = set()
        self.unique_operands = set()
        self.functions = []

    def halstead_vocab(self):
        return len(self.unique_operands) + len(self.unique_operators)
    
    def halstead_length(self):
        return self.operators + self.operands
    
    def halstead_estimated_length(self):
        return len(self.unique_operators) * math.log2(len(self.unique_operators)) + len(self.unique_operands) * math.log2(len(self.unique_operands))

    def halstead_volume(self):
        return self.halstead_length() * math.log2(self.halstead_vocab())
    
    def halstead_difficulty(self):
        if len(self.unique_operators) == 0 or len(self.unique_operands) == 0:
            return 0
        return (self.operators / 2) * (self.operands / len(self.unique_operands))
    
    def halstead_effort(self):
        return self.halstead_difficulty() * self.halstead_volume()
    
    def time_to_program(self):
        return self.halstead_effort() / 18 #in seconds
    
    def delivered_bugs(self):
        return (self.halstead_effort() ** (2/3)) / 3000

    def generic_visit(self, node: ast.AST):

        if node.__class__.__name__ in ['While', 'For', 'With', 'Try', 'TryExcept']:
            self.operators += 1
            self.unique_operators.add(node.__class__.__name__)
        
        super().generic_visit(node)

    def operand_helper(self, node: ast.AST):
        if isinstance(node, ast.Name):
            self.operands += 1
            print(node.id)
            self.unique_operands.add(node.id)
        if isinstance(node, ast.Constant):
            self.operands += 1
            print(node.value)
            self.unique_operands.add(node.value)
        if isinstance(node, ast.List):
            if len(node.elts) == 0:
                self.operands += 1
                self.unique_operands.add(str(node.elts))
            for elt in node.elts:
                self.operand_helper(elt)
        if isinstance(node, ast.Tuple):
            for elt in node.elts:
                self.operand_helper(elt)

    def operator_helper(self, node: ast.AST):
        self.operators += 1
        self.unique_operators.add(node.__class__.__name__)

    def visit_BoolOp(self, node: ast.BoolOp):
        # Boolean operations e.g. 'And', 'Not' etc.
        self.operator_helper(node.op)
        self.operands += len(node.values)
        for operand in node.values:
            if isinstance(operand, ast.Name):
                self.unique_operands.add(operand.id)

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        # Mathematical operands e.g. '+', '*' etc.
        self.operator_helper(node.op)

        self.operand_helper(node.left)
        self.operand_helper(node.right)

        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        # 
        self.operator_helper(node.op)

        self.operands += 1
        if isinstance(node.operand, ast.Constant):
            self.unique_operands.add(node.operand.value)
        if isinstance(node.operand, ast.Name):
            self.unique_operands.add(node.operand.id)

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # LHS of assignment
        self.operator_helper(node)
        self.operand_helper(node.targets[0])
        if isinstance(node.targets, ast.Tuple):
            for target in node.targets.elts:
                self.operand_helper(target)

        #RHS of assignment
        self.operand_helper(node.value)

        self.generic_visit(node)
        

    def visit_AugAssign(self, node: ast.AugAssign):
        # Augmented assignment (e.g., +=, -=, etc.)
        self.operators += 1
        self.unique_operators.add('AugAssign' + node.op.__class__.__name__)
        self.operand_helper(node.target)

        self.operand_helper(node.value)

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
        if isinstance(node.func, ast.Name):
            self.unique_operators.add(node.func.id)
        if isinstance(node.func, ast.Attribute):
            self.unique_operators.add(node.func.attr)
            if isinstance(node.func.value, ast.Name):
                self.operands += 1
                self.unique_operands.add(node.func.value.id)
        self.operands += len(node.args)
        for arg in node.args:
            if isinstance(arg, ast.Name):
                self.unique_operands.add(arg.id)
            if isinstance(arg, ast.Constant):
                self.unique_operands.add(arg.value)
            if isinstance(arg, ast.Expr):
                self.unique_operands.add(arg.value)
            
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self.operator_helper(node)

        if len(node.orelse) >= 1:
            if isinstance(node.orelse[0], ast.If):
                self.unique_operators.add('Elif')
            if not isinstance(node.orelse[0], ast.If):
                self.operators += 1
                self.unique_operators.add('Else')

        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        self.operator_helper(node)

        self.operands += 1
        if isinstance(node.value, ast.Name):
            self.unique_operands.add(node.value.id)

        if isinstance(node.slice, ast.Slice):
            if node.slice.lower is not None:
                self.operand_helper(node.slice.lower)
            if node.slice.upper is not None:
                self.operand_helper(node.slice.upper)

        self.generic_visit(node)


    def visit_FunctionDef(self, node: ast.FunctionDef):
        pass
    