import ast
from textwrap import dedent
from detectors.detect_long_function import LongFunctionDetector
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
import astpretty

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    visitor = CyclomaticComplexityVisitor()
    visitor.source_code = dedent(code).strip()
    visitor.visit(node)
    long_func_detector = LongFunctionDetector()
    long_func_detector.check_long_function(visitor.functions)
    print(long_func_detector.long_functions)
    print(visitor.functions)
    astpretty.pprint(node)

if __name__ == "__main__":
    main()