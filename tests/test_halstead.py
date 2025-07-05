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
        z = y - 1
        ''',
        (3 , 2, 3, 2)
    ),
    (
        '''
        y = x * 1
        ''',
        (3 , 2, 3, 2)
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
    (
        '''
        x = 1 + 2 * 3
        ''',
        (4, 3, 4, 3)
    ),
    (
        '''
        x or y
        ''',
        (2, 1, 2, 1)
    ),
    (
        '''
        while x < 5:
            print(x)
        ''',
        (3, 3, 2, 3)
    ),
    (
        '''
        x = 1
        if x > 1: 
            print(x)
        elif x < 1:
            print(x)
        else:
            print('hello world')
        ''',
        (9, 9, 3, 7)
    ),
    (
        '''
        x = 1
        if x > 1: 
            print(x)
        elif x < 1:
            print(x)
        elif x == 1:
            print(x)
        else:
            print('hello world')
        ''',
        (12, 12, 3, 8)
    ),
    (
        '''
        x = 1
        y = []
        if x > 1: 
            y.append(x)
        ''',
        (8, 5, 4, 4)
    ),
    (
        '''
        x,y = 1,2
        z = x * y
        ''',
        (7, 3, 5, 2)
    ),
    (
        '''
        z = 0
        x = [0,1,2,3,4,5,6]
        y = x[z:2]
        ''',
        (14, 4, 10, 2)
    ),
    ('''x.strip().lower()''',
    (1, 2, 1, 2)
    ),
    ('''
    x += y + 1
    ''',
    (3, 2, 3, 2)
    ),
    ('''
    ''',
    (0,0,0,0)
    )
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