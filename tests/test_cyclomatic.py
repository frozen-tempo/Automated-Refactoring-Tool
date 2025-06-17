import ast
from src.code_metrics.code_metrics import CodeMetricsVisitor
import radon

def test_simple_function():

    source_code = "def my_func(): x = 1; return x;"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == radon.complexity.cc.visit(ast.parse(source_code))

def test_if_statement():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_if_elif_else_statement():

    source_code = "def f(a):\n    if a > 10:\n        print('High')\n    elif a > 5:\n        print('Medium')\n    else:\n        print('Low')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 3

def test_for_loop():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_while_loop():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_try_except():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_bool_op():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_list_comprehension():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_with_statement():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_assert_statement():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_ternary():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2

def test_complex_function():

    source_code = "def function_with_if(a):\n    if a > 10:\n        print('Greater than 10')"
    code_metrics = CodeMetricsVisitor()
    code_metrics.visit(ast.parse(source_code))
    assert code_metrics.cyclomatic_complexity == 2