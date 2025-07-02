import ast
from src.code_metrics.cyclomatic import CyclomaticComplexityVisitor
import pytest
from textwrap import dedent

code_blocks = [
    (
        '''
        x = 1
        y = 2
        z = x + y
        ''',
        (),
        {}
    )
]