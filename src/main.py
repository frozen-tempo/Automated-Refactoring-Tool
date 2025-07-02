import ast
import pprint
import astor
from code_metrics.halstead import HalsteadMetricsVisitor
from radon.visitors import ComplexityVisitor

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    v = HalsteadMetricsVisitor()
    v.visit(node)
    print(v.unique_operators)
    print(v.unique_operands)
    #pprint.pprint(astor.dump_tree(node))

if __name__ == "__main__":
    main()