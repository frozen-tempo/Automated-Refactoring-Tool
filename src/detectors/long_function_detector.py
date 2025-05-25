import ast

class LongFunctionDetector:

    def __init__(self, max_function_lines = 20):
        self.max_function_lines = max_function_lines

    def check(self, node: ast.FunctionDef, violations):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, 'end_lineno') and node.end_lineno:
                function_length = node.end_lineno - node.lineno
            
            if function_length > self.max_function_lines:
                violations.append({
                    "Function Name:" : node.name,
                    "Line Number:" : node.lineno,
                    "Function Length:" : function_length,
                    "Code Smell Type:" : "Long Method"
            })