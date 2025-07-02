import ast
from src.code_metrics.halstead import HalsteadMetricsVisitor
import pytest
from textwrap import dedent

code_blocks = [
    (
        '''
        x = 1
        ''',
        (2 , 1, 2, 1)
    ), 
    (
        '''
        x = 1
        y = 2
        ''',
        (4 , 2, 4, 1)
    ),
    (
        '''
        x = 1
        y = x + 1
        ''',
        (5 , 3, 3, 2)
    ),
    (
        '''
        x = 0
        if x >= 1:
            print(x)
        ''',
        (5, 4, 3, 4)
    ),
    (
        '''
        x = 0
        if x >= 1:
            print(x)
        if x < 1: 
            str(x)
        ''',
        (8, 7, 3, 6)
    ),
]

@pytest.mark.parametrize("code,expected", code_blocks)
def test_code_blocks(code, expected):
    halstead_visitor = HalsteadMetricsVisitor()
    halstead_visitor.visit(ast.parse(dedent(code).strip()))
    assert expected == (halstead_visitor.operands, 
                        halstead_visitor.operators, 
                        len(halstead_visitor.unique_operands), 
                        len(halstead_visitor.unique_operators)
                        )