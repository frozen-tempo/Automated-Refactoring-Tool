import ast
import pprint
import astor
from code_metrics.cyclomatic import CyclomaticComplexityVisitor
from radon.visitors import ComplexityVisitor

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    v = CyclomaticComplexityVisitor()
    v.visit(node)

    pprint.pprint(astor.dump_tree(node))

if __name__ == "__main__":
    main()