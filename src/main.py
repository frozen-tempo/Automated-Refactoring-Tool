import ast
import astor
from code_metrics.cyclomatic import CyclomaticComplexityVisitor

def main():

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)

    visitor = CyclomaticComplexityVisitor()
    visitor.visit(node)
    for func in visitor.functions:
        print(f"Function: {func.name}, Complexity: {func.complexity}, Location: {func.start_lineno}") 

if __name__ == "__main__":
    main()