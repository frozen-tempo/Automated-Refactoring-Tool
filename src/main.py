import ast
import astor


def main():

    class Visitor(ast.NodeVisitor):

        def visit(self, node: ast.AST):
            print(f"Visiting node: {node.__class__.__name__}")
            self.generic_visit(node)

    with open('src/code_smells.py', 'r') as file:
        code = file.read()
    
    node = ast.parse(code)
    print(astor.dump_tree(node))

if __name__ == "__main__":
    main()