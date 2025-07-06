import ast
from src.detectors.detect_long_function import LongFunctionDetector, Function
import pytest
from textwrap import dedent

code_blocks = [
    (
        '''
        x = 1
        ''',
        ([])
    ),
    (
        '''
        def func():
            x = 1
            return x
        ''',
        ([
            Function(
                name='func',
                body= '''def func():
                            x = 1
                            return x''',
                mloc=2,
                complexity=1,
                num_params=0,
                num_localvar=1,
                branches=0,
                long_function=False
            )
        ])
    )
]

@pytest.mark.parametrize("code,expected", code_blocks)
def test_code_blocks(code, expected):
    longfunc_detector = LongFunctionDetector()
    longfunc_detector.visit(ast.parse(dedent(code).strip()))
    assert expected == (longfunc_detector.functions)