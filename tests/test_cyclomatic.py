import ast
from src.code_metrics.cyclomatic import CyclomaticComplexityVisitor
import pytest
from textwrap import dedent

code_blocks = [
    (
        '''
     if a: pass
     ''',
        2,
        {},
    ),
    (
        '''
     if a: pass
     else: pass
     ''',
        2,
        {},
    ),
    (
        '''
     if a: pass
     elif b: pass
     ''',
        3,
        {},
    ),
    (
        '''
     if a: pass
     elif b: pass
     else: pass
     ''',
        3,
        {},
    ),
    (
        '''
    if a and b: pass
    ''',
        3,
        {},
    ),
    (
        '''
    if a and b: pass
    else: pass
    ''',
        3,
        {},
    ),
    (
        '''
     if a and b: pass
     elif c and d: pass
     else: pass
     ''',
        5,
        {},
    ),
    (
        '''
     if a and b or c and d: pass
     else: pass
     ''',
        5,
        {},
    ),
    (
        '''
     if a and b or c: pass
     else: pass
     ''',
        4,
        {},
    ),
    (
        '''
     for x in range(10): print(x)
     ''',
        2,
        {},
    ),
    (
        '''
     for x in xrange(10): print(x)
     else: pass
     ''',
        3,
        {},
    ),
    (
        '''
     while a < 4: pass
     ''',
        2,
        {},
    ),
    (
        '''
     while a < 4: pass
     else: pass
     ''',
        3,
        {},
    ),
    (
        '''
     while a < 4 and b < 42: pass
     ''',
        3,
        {},
    ),
    (
        '''
     while a and b or c < 10: pass
     else: pass
     ''',
        5,
        {},
    ),
    # With and async-with statements no longer count towards CC, see #123
    (
        '''
     with open('raw.py') as fobj: print(fobj.read())
     ''',
        1,
        {},
    ),
    (
        '''
     [i for i in range(4)]
     ''',
        2,
        {},
    ),
    (
        '''
     [i for i in range(4) if i&1]
     ''',
        3,
        {},
    ),
    (
        '''
     (i for i in range(4))
     ''',
        2,
        {},
    ),
    (
        '''
     (i for i in range(4) if i&1)
     ''',
        3,
        {},
    ),
    (
        '''
     [i for i in range(42) if sum(k ** 2 for k in divisors(i)) & 1]
     ''',
        4,
        {},
    ),
    (
        '''
     try: raise TypeError
     except TypeError: pass
     ''',
        2,
        {},
    ),
    (
        '''
     try: raise TypeError
     except TypeError: pass
     else: pass
     ''',
        3,
        {},
    ),
    (
        '''
     try: raise TypeError
     finally: pass
     ''',
        1,
        {},
    ),
    (
        '''
     try: raise TypeError
     except TypeError: pass
     finally: pass
     ''',
        2,
        {},
    ),
    (
        '''
     try: raise TypeError
     except TypeError: pass
     else: pass
     finally: pass
     ''',
        3,
        {},
    ),
    (
        '''
     try: raise TypeError
     except TypeError: pass
     else:
        pass
        pass
     finally: pass
     ''',
        3,
        {},
    ),
    # Lambda are not counted anymore as per #68
    (
        '''
     k = lambda a, b: k(b, a)
     ''',
        1,
        {},
    ),
    (
        '''
     k = lambda a, b, c: c if a else b
     ''',
        2,
        {},
    ),
    (
        '''
     v = a if b else c
     ''',
        2,
        {},
    ),
    (
        '''
     v = a if sum(i for i in xrange(c)) < 10 else c
     ''',
        3,
        {},
    ),
    (
        '''
     sum(i for i in range(12) for z in range(i ** 2) if i * z & 1)
     ''',
        4,
        {},
    ),
    (
        '''
     sum(i for i in range(10) if i >= 2 and val and val2 or val3)
     ''',
        6,
        {},
    ),
    (
        '''
     for i in range(10):
         print(i)
     else:
         print('wah')
         print('really not found')
         print(3)
     ''',
        3,
        {},
    ),
    (
        '''
     while True:
         print(1)
     else:
         print(2)
         print(1)
         print(0)
         print(-1)
     ''',
        3,
        {},
    ),
    (
        '''
     assert i < 0
     ''',
        1,
        {},
    ),
    (
        '''
     def f():
        assert 10 > 20
     ''',
        1,
        {},
    ),
    (
        '''
     class TestYo(object):
        def test_yo(self):
            assert self.n > 4
     ''',
        1,
        {},
    ),
        (
        '''
     match a:
         case 1: pass
     ''',
        2,
        {},
    ),
    (
        '''
     match a:
         case 1: pass
         case _: pass
     ''',
        2,
        {},
    ),
    (
        '''
     match a:
         case 1: pass
         case 2: pass
     ''',
        3,
        {},
    ),
    (
        '''
     match a:
         case 1: pass
         case 2: pass
         case _: pass
     ''',
        3,
        {},
    ),
]

@pytest.mark.parametrize("code,expected, kwargs", code_blocks)
def test_code_blocks(code, expected,kwargs):
    comp_visitor = CyclomaticComplexityVisitor()
    comp_visitor.visit(ast.parse(dedent(code).strip()))
    assert comp_visitor.cyclomatic_complexity == expected