import ast
from textwrap import dedent
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
class LongFunctionDetector:

    def __init__(self):
        self.long_functions = []
        self.source_code = ""

    def check_long_function(self, functions):

        for func in functions:
            if (func.mloc > 50) or (func.complexity > 5) or (((func.num_params > 5) or (func.num_localvar > 10)) and func.branches > 4):
                func.long_function = True
                self.long_functions.append(func)
            