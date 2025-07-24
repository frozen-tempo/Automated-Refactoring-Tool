import ast
from code_metrics.func import Function
from code_metrics.cls import Class
    
class CyclomaticComplexityVisitor(ast.NodeVisitor):

    def __init__(self, starting_complexity = 1, func_to_method=False, classname=None, location =0, source_code=""):
        self.cyclomatic_complexity = starting_complexity
        self.functions = []
        self.classes = []
        self.func_to_method = func_to_method
        self.classname = classname
        self.location = location
        self.source_code = source_code
        self.num_localvar = set()
        self.branches = 0
        self.mloc = set()

    def get_nodename(self, node: ast.AST):
        return node.__class__.__name__
    
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
        )
    
    def get_total_loc(self):

        module_loc = len(self.mloc)
        function_loc = sum(func.mloc for func in self.functions)
        class_loc = sum(cls.mloc for cls in self.classes)

        return module_loc + function_loc + class_loc

    def generic_visit(self, node: ast.AST):

        if isinstance(node, (
            ast.Return, ast.Delete, ast.Assign, ast.AugAssign, ast.AnnAssign,
            ast.For, ast.AsyncFor, ast.While, ast.If, ast.With, ast.AsyncWith,
            ast.Raise, ast.Try, ast.Assert, ast.Import, ast.ImportFrom,
            ast.Global, ast.Nonlocal, ast.Expr, ast.Pass, ast.Break, ast.Continue,
            ast.Match
        )):
            lineno = getattr(node, 'lineno', None)
            if lineno is not None:
                self.mloc.add(lineno)
        
        # For AST node, 'try' blocks are characterised with handlers (except) and orelse (else)
        if isinstance(node, (ast.Try)):
            self.cyclomatic_complexity += len(node.handlers) + bool(node.orelse)
        # For AST node, 'if' can be counted each time as it appears with orelse as well as the start of the conditional block
        elif isinstance(node, (ast.If, ast.IfExp)):
            self.cyclomatic_complexity += 1
            self.branches += 1
            
            if isinstance(node.orelse, list) and len(node.orelse) >= 1 and hasattr(node.orelse[0], 'lineno') and not isinstance(node.orelse[0], ast.If):
                self.mloc.add(node.orelse[0].lineno - 1)

        # Count each of the values for a 'BoolOp' node as a decision point, default path is not counted therefore - 1
        elif isinstance(node, (ast.BoolOp)):
            self.cyclomatic_complexity += len(node.values) - 1
        # For AST node, 'for', 'while' and 'AsyncFor' are counted as decision points, these could contain orelse so this is counted
        # also if it exists 
        elif isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
            self.cyclomatic_complexity += bool(node.orelse) + 1
        # For AST node, 'comprehension' nodes count the number of 'ifs' or test expressions + 1
        elif isinstance(node, (ast.comprehension)):
            self.cyclomatic_complexity += len(node.ifs) + 1
        # For AST node, 'match' is counted as a decision point, this could contain orelse so this is counted, underscore/wildcard cases are considered
        # as 'else' so are not counted
        elif isinstance(node, (ast.Match)):
            wildcard_cases = sum(1 for case in node.cases if isinstance(case.__getattribute__('pattern'), ast.MatchAs) and case.pattern is None)
            self.cyclomatic_complexity += (len(node.cases) - wildcard_cases) if (len(node.cases) - wildcard_cases) > 0 else 0
            
        super().generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self.cyclomatic_complexity += 1

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.num_localvar.add(target.id)
            elif isinstance(target, (ast.Tuple, ast.List)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.num_localvar.add(elt.id)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):

        function_closures = []
        function_complexity = 1
        params = []
        for param in node.args.args:
            params.append(param.arg)
        num_localvar = set()
        branches = 0
        func_loc = set()

        if hasattr(node, 'lineno'):
            func_loc.add(node.lineno)

        cyclomatic_visitor = CyclomaticComplexityVisitor(starting_complexity=0)

        for child in node.body:

            # Careful not double count the +1 complexity for the function itself, set the starting complexity to 0
            cyclomatic_visitor.visit(child)
            function_closures.extend(cyclomatic_visitor.functions)
            function_complexity += cyclomatic_visitor.cyclomatic_complexity

            branches += cyclomatic_visitor.branches

            # Check if variables found are not parameters of the function
            for localvar in cyclomatic_visitor.num_localvar:
                if localvar not in params:
                    num_localvar.add(localvar)

        func_loc.update(cyclomatic_visitor.mloc)

        func = Function(
            node.name,
            ast.get_source_segment(self.source_code, node) if self.source_code else "",
            node.lineno,
            node.end_lineno if hasattr(node, 'end_lineno') else self.get_location(),
            self.func_to_method,
            self.classname if self.func_to_method else None,
            function_closures,
            function_complexity,
            len(func_loc),
            len(node.args.args),
            len(num_localvar),
            branches
        )
        self.functions.append(func)

    def visit_ClassDef(self, node: ast.ClassDef):
        
        class_name = node.name
        class_complexity = 0
        methods = []
        cls_loc = set()

        lineno = getattr(node, 'lineno', None)
        if lineno is not None:
            cls_loc.add(lineno)

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
            
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                cls_loc.update(cyclomatic_visitor.mloc)
    

        method_loc = sum(method.mloc for method in methods)
        class_loc = len(cls_loc) + method_loc

        cls = Class(
                class_name,
                node.lineno,
                node.end_lineno if hasattr(node, 'end_lineno') else self.get_location(),
                methods,
                class_complexity,
                class_loc

        )
        
        self.classes.append(cls)