import ast
import pprint
import astor
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
from radon.visitors import ComplexityVisitor

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    visitor = CyclomaticComplexityVisitor()
    visitor.visit(node)

    v2 = ComplexityVisitor.from_ast(node)

    for func in v2.functions:
        print(f"RadonFunction: {func.name}, Complexity: {func.complexity}")
    for cls in v2.classes:
        print(f"RadonClass: {cls.name}, Complexity: {cls.real_complexity}")

    # pprint.pprint(astor.dump_tree(node))

if __name__ == "__main__":
    main()