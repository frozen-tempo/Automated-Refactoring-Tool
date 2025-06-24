import ast

class Function:
    
    def __init__(self, name, start_lineno, end_lineno, is_method, belongs_to, complexity):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.is_method = is_method
        self.belongs_to = belongs_to
        self.complexity = complexity

    def get_name(self):

        if self.belongs_to is None:
            return self.name
        else:
            return f"{self.belongs_to}.{self.name}"
        
    def __str__(self):
        return f"Class: {self.name} \n 
                Start Line: {self.start_lineno} \n 
                End Line: {self.end_lineno} \n 
                Belongs to: {self.belongs_to} \n 
                Complexity: {self.complexity}"
        
class Class:

    def __init__(self, name, start_lineno, end_lineno, complexity):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.methods = []
        self.complexity = complexity

    def __str__(self):
        return f"Class: {self.name} \n 
                Start Line: {self.start_lineno} \n 
                End Line: {self.end_lineno} \n 
                Methods: {self.methods} \n 
                Complexity: {self.complexity}"
    
class CodeMetricsVisitor(ast.NodeVisitor):

    def get_nodename(self, node: ast.AST):
        return node.__class__.__name__
    
class CyclomaticComplexityVisitor(CodeMetricsVisitor):

    def __init__(self, func_to_method=False, classname=None):

        self.cyclomatic_complexity = 1
        self.functions = []
        self.classes = []
        self.func_to_method = func_to_method
        self.classname = classname

    def function_complexity(self):
        if not self.functions:
            return 0
        return sum(map(self.functions.get, 'complexity', self.functions)) - len(self.functions)
    
    def class_complexity(self):
        if not self.classes:
            return 0
        return sum(map(self.classes.get, 'complexity', self.classes)) - len(self.classes)
    
    def total_complexity(self):
        return (
            self.complexity 
            + self.function_complexity() 
            + self.class_complexity() 
            + 1
        )

    def generic_visit(self, node: ast.AST):

        # Get the name of the node currently being visited
        name = self.get_nodename(node)
        # For AST node, 'try' blocks are characterised with handlers (except) and orelse (else)
        if name in ('Try', 'TryExcept'):
            self.cyclomatic_complexity += len(node.handlers) + bool(node.orelse)
        # For AST node, 'if' can be counted each time as it appears with orelse as well as the start of the conditional block
        elif name in ('If', 'IfExp'):
            self.cyclomatic_complexity += 1
        # Count each of the values for a 'BoolOp' node as a decision point, default path is not counted therefore - 1
        elif name == 'BoolOp':
            self.cyclomatic_complexity += len(node.values) - 1
        # For AST node, 'for', 'while' and 'AsyncFor' are counted as decision points, these could contain orelse so this is counted
        # also if it exists 
        elif name in ('For', 'While', 'AsyncFor'):
            self.cyclomatic_complexity += bool(node.orelse) + 1
        # For AST node, 'comprehension' nodes count the number of 'ifs' or test expressions + 1
        elif name == 'comprehension':
            self.cyclomatic_complexity += len(node.ifs) + 1
        # For AST node, 'match' is counted as a decision point, this could contain orelse so this is counted, underscore cases are considered
        # as 'else' so are not counted
        elif name == "match":
            underscore_cases = sum(1 for case in node.cases if isinstance(case.__getattribute__('pattern'), ast.MatchAs) and case.pattern.name is None)
            self.cyclomatic_complexity += (len(node.cases) - underscore_cases) if (len(node.cases) - underscore_cases) > 0 else 0

        