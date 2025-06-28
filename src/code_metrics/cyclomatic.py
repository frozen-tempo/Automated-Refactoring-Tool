import ast

class Function:
    
    def __init__(self, name, start_lineno, end_lineno, is_method, belongs_to, closures, complexity):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.is_method = is_method
        self.belongs_to = belongs_to
        self.closures = closures
        self.complexity = complexity

    def get_name(self):

        if self.belongs_to is None:
            return self.name
        else:
            return f"{self.belongs_to}.{self.name}"
        
    def __str__(self):
        return f"Function: {self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Belongs to: {self.belongs_to} \n Complexity: {self.complexity}"

    def __repr__(self):
        return f"Function: ({self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Belongs to: {self.belongs_to} \n Complexity: {self.complexity} \n)"


class Class:

    def __init__(self, name, start_lineno, end_lineno, methods, complexity):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.methods = methods
        self.complexity = complexity

    def avg_method_complexity(self):
        return sum(methd.complexity for methd in self.methods) / len(self.methods)

    def __str__(self):
        return f"Class:{self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Methods: {self.methods} \n Complexity: {self.complexity} \n Avg Complexity: {self.avg_method_complexity()}"
    
    def __repr__(self):
        return f"Class:({self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Methods: \n {self.methods} \n Complexity: {self.complexity} \n Avg Complexity: {self.avg_method_complexity()})"
    
class CodeMetricsVisitor(ast.NodeVisitor):

    def get_nodename(self, node: ast.AST):
        return node.__class__.__name__
    
    def get_name(self, node: ast.AST):
        if hasattr(node, 'name'):
            return node.name
        elif hasattr(node, 'id'):
            return node.id
        return None
    
class CyclomaticComplexityVisitor(CodeMetricsVisitor):

    def __init__(self, starting_complexity = 1, func_to_method=False, classname=None):

        self.cyclomatic_complexity = starting_complexity
        self.functions = []
        self.classes = []
        self.func_to_method = func_to_method
        self.classname = classname
        self.location = 0
    
    def get_location(self):
        return self.location
    
    def set_location(self, lineno):
        if lineno > self.location:
            self.location = lineno

    def function_complexity(self):
        if not self.functions:
            return 0
        return sum(func.complexity for func in self.functions) - len(self.functions)
    
    def class_complexity(self):
        if not self.classes:
            return 0
        return sum(cls.complexity for cls in self.classes) - len(self.classes)
    
    def total_complexity(self):
        return (
            self.cyclomatic_complexity 
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
        # For AST node, 'match' is counted as a decision point, this could contain orelse so this is counted, underscore/wildcard cases are considered
        # as 'else' so are not counted
        elif name == "Match":
            wildcard_cases = sum(1 for case in node.cases if isinstance(case.__getattribute__('pattern'), ast.MatchAs) and case.pattern.name is None)
            self.cyclomatic_complexity += (len(node.cases) - wildcard_cases) if (len(node.cases) - wildcard_cases) > 0 else 0

        super().generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self.cyclomatic_complexity += 1

    def visit_FunctionDef(self, node: ast.FunctionDef):

        function_closures = []
        function_complexity = 1

        for child in node.body:

            # Careful not double count the +1 complexity for the function itself, set the starting complexity to 0
            cyclomatic_visitor = CyclomaticComplexityVisitor(starting_complexity=0)
            cyclomatic_visitor.visit(child)
            function_closures.extend(cyclomatic_visitor.functions)
            function_complexity += cyclomatic_visitor.cyclomatic_complexity

        func = Function(
            node.name,
            node.lineno,
            node.end_lineno if hasattr(node, 'end_lineno') else self.get_location(),
            self.func_to_method,
            self.classname if self.func_to_method else None,
            function_closures,
            function_complexity
        )
        self.functions.append(func)
        for func in self.functions:
            print(f"Function: {func.name}, Complexity: {func.complexity}")
    

    def visit_ClassDef(self, node: ast.ClassDef):
        
        class_name = self.get_name(node)
        class_complexity = 0
        methods = []

        for child in node.body:
            
            cyclomatic_visitor = CyclomaticComplexityVisitor(
                starting_complexity=0, 
                func_to_method=True, 
                classname=class_name
            )
            cyclomatic_visitor.visit(child)
            methods.extend(cyclomatic_visitor.functions)
            class_complexity += (cyclomatic_visitor.cyclomatic_complexity 
                                + cyclomatic_visitor.function_complexity()
                                + len(cyclomatic_visitor.functions))

        cls = Class(
                class_name,
                node.lineno,
                node.end_lineno if hasattr(node, 'end_lineno') else self.get_location(),
                methods,
                class_complexity
        )

        self.classes.append(cls) 