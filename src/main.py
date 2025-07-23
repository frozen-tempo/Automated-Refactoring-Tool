import ast
from textwrap import dedent
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
import astpretty

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)
    function_length = 0
    class_length = 0
    visitor = CyclomaticComplexityVisitor()
    visitor.source_code = dedent(code).strip()
    visitor.visit(node)
    for func in visitor.functions:
        function_length += func.mloc
    
    for cls in visitor.classes:
        for method in cls.methods:
            class_length += method.mloc
    
    #print(visitor.functions)
    #print(visitor.classes)
    print(f"Total function MLOC: {function_length}")
    print(f"Total class MLOC: {class_length}")
    print(visitor.get_total_loc())
    #long_func_detector = LongFunctionDetector()
    #long_func_detector.check_long_function(visitor.functions)
    #print(long_func_detector.long_functions)
    #print(visitor.functions)
    #astpretty.pprint(node)

if __name__ == "__main__":
    main()