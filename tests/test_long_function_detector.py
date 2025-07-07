import ast
from src.code_metrics.cyclomatic import CyclomaticComplexityVisitor
from src.detectors.detect_long_function import LongFunctionDetector
from src.code_metrics.func import Function
import pytest
from textwrap import dedent

code_blocks = [
    # No functions in code
    (
        '''
        x = 1
        ''',
        ([])
    ),
    # Short function
    (
        '''
        def func():
            x = 1
            return x
        ''',
        ([])
    ),
    # Function with > 50 lines of code
    (
       '''def long_function():
            val = 0
            val = val + 1  # Line 1
            val = val + 1  # Line 2
            val = val + 1  # Line 3
            val = val + 1  # Line 4
            val = val + 1  # Line 5
            val = val + 1  # Line 6
            val = val + 1  # Line 7
            val = val + 1  # Line 8
            val = val + 1  # Line 9
            val = val + 1  # Line 10
            val = val * 2  # Line 11
            val = val * 2  # Line 12
            val = val - 5  # Line 13
            val = val - 5  # Line 14
            val = val / 2  # Line 15
            val = val / 2  # Line 16
            val = val + 10 # Line 17
            val = val + 10 # Line 18
            val = val * 3  # Line 19
            val = val - 1  # Line 20
            val = val - 1  # Line 21
            val = val - 1  # Line 22
            val = val - 1  # Line 23
            val = val - 1  # Line 24
            val = val - 1  # Line 25
            val = val - 1  # Line 26
            val = val - 1  # Line 27
            val = val - 1  # Line 28
            val = val - 1  # Line 29
            val = val - 1  # Line 30
            val = val - 1  # Line 31
            val = val - 1  # Line 32
            val = val - 1  # Line 33
            val = val - 1  # Line 34
            val = val - 1  # Line 35
            val = val - 1  # Line 36
            val = val - 1  # Line 37
            val = val - 1  # Line 38
            val = val - 1  # Line 39
            val = val - 1  # Line 40
            val = val - 1  # Line 41
            val = val - 1  # Line 42
            val = val - 1  # Line 43
            val = val - 1  # Line 44
            val = val - 1  # Line 45
            val = val - 1  # Line 46
            val = val - 1  # Line 47
            val = val - 1  # Line 48
            val = val - 1  # Line 49
            val = val - 1  # Line 50
            return val
            ''',
            ([
            {"name": 'long_function',
            "start_lineno": 1,
            "end_lineno": 53,
            "is_method": False,
            "belongs_to": None,
            "closures": [],
            "complexity": 1,
            "mloc": 52,
            "num_params": 0,
            "num_localvar": 1,
            "branches": 0,
            "long_function": True
            }])
    ),
    # Function with > 5 cyclomatic complexity
    ('''def complex_function(input_value):
        if input_value == 1:
            return "One"
        elif input_value == 2:
            return "Two"
        elif input_value == 3:
            return "Three"
        elif input_value == 4:
            return "Four"
        elif input_value == 5:
            return "Five"
        else:
            return "Other"
    '''
    ,
    [
        {
        "name": 'complex_function',
        "start_lineno": 1,
        "end_lineno": 13,
        "is_method": False,
        "belongs_to": None,
        "closures": [],
        "complexity": 6,
        "mloc": 12,
        "num_params": 1,
        "num_localvar": 0,
        "branches": 5,
        "long_function": True
        }
    ]
    ),
    # Function with > 4 params
    ('''def too_many_params_function(x, y, z, a, b):
            if x == 1:
                print(x)
            if y == 2:
                print(y)
            if z == 3:
                print(z)
            if a == 4:
                print(a)
            if b == 5:
                print(b)
    '''
    ,
    [
        {
        "name": 'too_many_params_function',
        "start_lineno": 1,
        "end_lineno": 11,
        "is_method": False,
        "belongs_to": None,
        "closures": [],
        "complexity": 6,
        "mloc": 10,
        "num_params": 5,
        "num_localvar": 0,
        "branches": 5,
        "long_function": True
        }
    ]
    )
]

@pytest.mark.parametrize("code,expected", code_blocks)
def test_code_blocks(code, expected):
    node = ast.parse(dedent(code).strip())
    visitor = CyclomaticComplexityVisitor()
    visitor.source_code = code.strip()
    visitor.visit(node)
    long_func_detector = LongFunctionDetector()
    long_func_detector.check_long_function(visitor.functions)
    assert expected == (long_func_detector.long_functions)