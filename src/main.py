import ast
import pprint
import astor
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
from radon.visitors import ComplexityVisitor

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    v1 = CyclomaticComplexityVisitor()
    v1.visit(node)

    for func in v1.functions:
        print(f"Function: {func.name}, Complexity: {func.complexity}")
    for cls in v1.classes:
        print(f"Class: {cls.name}, Complexity: {cls.complexity}")


    v2 = ComplexityVisitor.from_ast(node)
    v2.visit(node)

    for func in v2.functions:
        print(f"RadonFunction: {func.name}, Complexity: {func.complexity}")
    for cls in v2.classes:
        print(f"RadonClass: {cls.name}, Complexity: {cls.complexity}")

    # pprint.pprint(astor.dump_tree(node))

if __name__ == "__main__":
    main()