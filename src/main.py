import ast
import astor

def main():

    class DetectionASTVisitor(ast.NodeVisitor):
        def __init__(self):
            self.violations = []

        def visit(self, node: ast.AST):
            LongFunctionDetector().check(node,self.violations)
            WithOpenDetector().check(node, self.violations)
            WildcardImportDetector().check(node, self.violations)
            self.generic_visit(node)

            return self.violations

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
    class WithOpenDetector:

        def __init__(self):
            self.open_exists = False
            self.with_exists = False
            self.location = None

        def check(self, node: ast.FunctionDef, violations):

            if isinstance(node, ast.FunctionDef):
                self.location = node.lineno

                for ast_child_node in ast.walk(node):
                    if isinstance(ast_child_node, ast.Name) and ast_child_node.id == 'open':
                        self.open_exists = True
                    if isinstance(ast_child_node, ast.With):
                        self.with_exists= True

            if self.open_exists and not self.with_exists:
                    violations.append({
                        "Line Number:" : self.location,
                        "Code Smell Type:" : "Using Open w/o With"
            })
    
    class WildcardImportDetector:

        def __init__(self):
            self.location = None

        def check(self, node:ast.ImportFrom, violations):
            if isinstance(node, ast.ImportFrom):
                self.location = node.lineno
                for alias in node.names:
                    if alias.name == "*":
                        violations.append({
                        "Line Number:" : self.location,
                        "Code Smell Type:" : "Wildcard Import"
                        })

    
    class BadTruthyFalsyDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class UnpythonicLoopDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class ListComprehensionAntiIdiomDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class GlobalVariableDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class FeatureEnvyDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class MagicNumberDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class DuplicatedCodeDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class LongParameterListDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class NestedConditionalDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass
    
    class DeadCodeDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    class ShotgunSurgeryDetector:

        def __init__(self):
            pass

        def check(self, node, violations):
            pass

    with open('code_smells.py') as file:
        code = file.read()
    ast_node = ast.parse(code)

    parser = DetectionASTVisitor()
    parser.visit(ast_node)

    print(parser.violations)
    #print(astor.dump_tree(ast_node))

if __name__ == "__main__":
    main()
