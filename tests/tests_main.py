import pytest
from src.main import DetectionASTVisitor
import ast

@pytest.mark.parametrize("code,expected", ['long_functions.py',"'"])

def test_long_function_detection(code_file, expected):
    
    with open (code_file,'r') as file:
        code = file.read()
    ast_node = ast.parse(code)

    parser = DetectionASTVisitor()
    assert parser.visit(ast_node) == expected
    