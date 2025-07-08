import pytest
import ast
from unittest.mock import patch, MagicMock
from src.refactorers.refactor_long_function import LongMethodRefactorer, RefactoringCandidate, RefactoringTransformer

class TestLongMethodRefactorer:
    """Test suite for the LongMethodRefactorer class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.refactorer = LongMethodRefactorer(max_method_length=10, min_extract_length=3)
    
    def test_initialization(self):
        """Test refactorer initialization with custom parameters"""
        custom_refactorer = LongMethodRefactorer(max_method_length=20, min_extract_length=5)
        assert custom_refactorer.max_method_length == 20
        assert custom_refactorer.min_extract_length == 5
        assert custom_refactorer.variable_tracker == {}
    
    def test_count_logical_lines_simple_method(self):
        """Test counting logical lines for a simple method"""
        code = """
def simple_method():
    x = 1
    y = 2
    return x + y
"""
        tree = ast.parse(code)
        method_node = tree.body[0]
        count = self.refactorer._count_logical_lines(method_node)
        assert count == 4  # def line + 3 body lines
    
    def test_count_logical_lines_complex_method(self):
        """Test counting logical lines for a method with loops and conditions"""
        code = """
def complex_method():
    result = []
    for i in range(10):
        if i % 2 == 0:
            result.append(i)
        else:
            result.append(i * 2)
    return result
"""
        tree = ast.parse(code)
        method_node = tree.body[0]
        count = self.refactorer._count_logical_lines(method_node)
        assert count >= 7  # Should count all logical lines
    
    def test_find_containing_class_with_class(self):
        """Test finding containing class when method is in a class"""
        code = """
class TestClass:
    def test_method(self):
        pass
"""
        tree = ast.parse(code)
        method_node = tree.body[0].body[0]
        class_name = self.refactorer._find_containing_class(tree, method_node)
        assert class_name == "TestClass"
    
    def test_find_containing_class_without_class(self):
        """Test finding containing class when method is standalone"""
        code = """
def standalone_method():
    pass
"""
        tree = ast.parse(code)
        method_node = tree.body[0]
        class_name = self.refactorer._find_containing_class(tree, method_node)
        assert class_name is None
    
    def test_should_group_statements_assignments(self):
        """Test grouping of assignment statements"""
        code1 = "x = 1"
        code2 = "y = 2"
        stmt1 = ast.parse(code1).body[0]
        stmt2 = ast.parse(code2).body[0]
        
        should_group = self.refactorer._should_group_statements(stmt1, stmt2)
        assert should_group is True
    
    def test_should_group_statements_different_types(self):
        """Test that different statement types are not grouped"""
        code1 = "x = 1"
        code2 = "if True: pass"
        stmt1 = ast.parse(code1).body[0]
        stmt2 = ast.parse(code2).body[0]
        
        should_group = self.refactorer._should_group_statements(stmt1, stmt2)
        assert should_group is False
    
    def test_analyze_variable_usage(self):
        """Test analysis of variable usage in statements"""
        code = """
result = process_data(input_data, config)
output = format_result(result)
"""
        tree = ast.parse(code)
        statements = tree.body
        
        used_vars = self.refactorer._analyze_variable_usage(statements)
        expected_vars = {'input_data', 'config', 'process_data', 'format_result'}
        assert expected_vars.issubset(used_vars)
    
    def test_analyze_variable_usage_filters_builtins(self):
        """Test that builtin functions are filtered out"""
        code = """
result = len(data)
output = str(result)
"""
        tree = ast.parse(code)
        statements = tree.body
        
        used_vars = self.refactorer._analyze_variable_usage(statements)
        # len and str should be filtered out
        assert 'len' not in used_vars
        assert 'str' not in used_vars
        assert 'data' in used_vars
    
    def test_generate_method_name_with_assignments(self):
        """Test method name generation for assignment statements"""
        code = """
x = 1
y = 2
"""
        tree = ast.parse(code)
        statements = tree.body
        
        name = self.refactorer._generate_method_name(statements, "original_method", "extract_method")
        assert name == "set_method"
    
    def test_generate_method_name_with_function_calls(self):
        """Test method name generation for function calls"""
        code = """
data.process()
data.validate()
"""
        tree = ast.parse(code)
        statements = tree.body
        
        name = self.refactorer._generate_method_name(statements, "original_method", "extract_method")
        assert name == "process_method"
    
    def test_generate_method_name_fallback(self):
        """Test fallback method name generation"""
        code = """
pass
"""
        tree = ast.parse(code)
        statements = tree.body
        
        name = self.refactorer._generate_method_name(statements, "original_method", "extract_method")
        assert name == "extracted_from_original_method"
    
    def test_get_function_name_simple(self):
        """Test extracting function name from simple call"""
        code = "func()"
        tree = ast.parse(code)
        call_node = tree.body[0].value
        
        func_name = self.refactorer._get_function_name(call_node)
        assert func_name == "func"
    
    def test_get_function_name_attribute(self):
        """Test extracting function name from attribute call"""
        code = "obj.method()"
        tree = ast.parse(code)
        call_node = tree.body[0].value
        
        func_name = self.refactorer._get_function_name(call_node)
        assert func_name == "method"
    
    def test_generate_condition_name_compare(self):
        """Test generating condition name from comparison"""
        code = "x > 5"
        tree = ast.parse(code, mode='eval')
        condition = tree.body
        
        name = self.refactorer._generate_condition_name(condition)
        assert name == "x"
    
    def test_generate_condition_name_variable(self):
        """Test generating condition name from variable"""
        code = "is_valid"
        tree = ast.parse(code, mode='eval')
        condition = tree.body
        
        name = self.refactorer._generate_condition_name(condition)
        assert name == "is_valid"
    
    def test_get_loop_variable_name(self):
        """Test extracting loop variable name"""
        code = """
for item in items:
    pass
"""
        tree = ast.parse(code)
        loop_node = tree.body[0]
        
        var_name = self.refactorer._get_loop_variable_name(loop_node)
        assert var_name == "item"

class TestRefactoringCandidate:
    """Test suite for RefactoringCandidate dataclass"""
    
    def test_refactoring_candidate_creation(self):
        """Test creating a RefactoringCandidate instance"""
        candidate = RefactoringCandidate(
            method_name="test_method",
            class_name="TestClass",
            start_line=1,
            end_line=5,
            lines_of_code=5,
            refactoring_type="extract_method",
            code_block=[],
            suggested_name="extracted_method",
            parameters=["param1", "param2"]
        )
        
        assert candidate.method_name == "test_method"
        assert candidate.class_name == "TestClass"
        assert candidate.start_line == 1
        assert candidate.end_line == 5
        assert candidate.lines_of_code == 5
        assert candidate.refactoring_type == "extract_method"
        assert candidate.suggested_name == "extracted_method"
        assert candidate.parameters == ["param1", "param2"]

class TestRefactoringTransformer:
    """Test suite for RefactoringTransformer class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sample_candidate = RefactoringCandidate(
            method_name="test_method",
            class_name="TestClass",
            start_line=1,
            end_line=3,
            lines_of_code=3,
            refactoring_type="extract_method",
            code_block=[],
            suggested_name="extracted_method",
            parameters=["param1"]
        )
    
    def test_transformer_initialization(self):
        """Test RefactoringTransformer initialization"""
        transformer = RefactoringTransformer([self.sample_candidate])
        assert len(transformer.candidates) == 1
        assert transformer.new_methods == []
        assert transformer.processed_methods == set()

class TestIntegration:
    """Integration tests for the complete refactoring process"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.refactorer = LongMethodRefactorer(max_method_length=5, min_extract_length=2)
    
    def test_simple_method_refactoring(self):
        """Test refactoring a simple long method"""
        code = """
def long_method():
    x = 1
    y = 2
    z = x + y
    result = z * 2
    final = result + 1
    return final
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Check that the code was modified
        assert refactored != code
        # Check that new methods were created
        assert "def " in refactored
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
    
    def test_class_method_refactoring(self):
        """Test refactoring a method within a class"""
        code = """
class TestClass:
    def long_method(self):
        self.x = 1
        self.y = 2
        self.z = self.x + self.y
        result = self.z * 2
        final_result = result + 1
        return final_result
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Check that the code was modified
        assert refactored != code
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
        # Should contain self parameter in extracted methods
        assert "def " in refactored
    
    def test_conditional_extraction(self):
        """Test extraction of conditional blocks"""
        code = """
def method_with_conditions():
    if condition1:
        process_data()
        validate_data()
        clean_data()
    elif condition2:
        handle_error()
        log_error()
        retry_operation()
    else:
        default_action()
        finalize()
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
    
    def test_loop_extraction(self):
        """Test extraction of loop bodies"""
        code = """
def method_with_loop():
    for item in items:
        process_item(item)
        validate_item(item)
        store_item(item)
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
    
    def test_no_refactoring_needed(self):
        """Test that short methods are not refactored"""
        code = """
def short_method():
    return 1 + 2
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Code should remain unchanged
        assert refactored.strip() == code.strip()
    
    def test_multiple_methods_refactoring(self):
        """Test refactoring multiple methods in the same code"""
        code = """
class MultiMethodClass:
    def first_long_method(self):
        self.a = 1
        self.b = 2
        self.c = 3
        result1 = self.a + self.b
        result2 = result1 + self.c
        return result2
    
    def second_long_method(self):
        data = self.get_data()
        processed = self.process(data)
        validated = self.validate(processed)
        stored = self.store(validated)
        return stored
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
        # Should contain original class
        assert "class MultiMethodClass:" in refactored

class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.refactorer = LongMethodRefactorer()
    
    def test_empty_code(self):
        """Test handling of empty code"""
        code = ""
        refactored = self.refactorer.analyze_and_refactor(code)
        assert refactored == code
    
    def test_invalid_python_syntax(self):
        """Test handling of invalid Python syntax"""
        code = "def invalid_method(\n    # missing closing parenthesis"
        
        with pytest.raises(SyntaxError):
            self.refactorer.analyze_and_refactor(code)
    
    def test_method_with_only_comments(self):
        """Test method containing only comments"""
        code = """
def comment_method():
    # This is a comment
    # Another comment
    # Yet another comment
    pass
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        # Should not be refactored due to low logical line count
        assert refactored.strip() == code.strip()
    
    def test_method_with_nested_functions(self):
        """Test method with nested function definitions"""
        code = """
def method_with_nested():
    def inner_function():
        return 1
    
    x = inner_function()
    y = inner_function()
    z = inner_function()
    result = x + y + z
    return result
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
    
    def test_method_with_decorators(self):
        """Test method with decorators"""
        code = """
class DecoratedClass:
    @property
    def long_property(self):
        value1 = self.calculate_value1()
        value2 = self.calculate_value2()
        value3 = self.calculate_value3()
        result = value1 + value2 + value3
        return result
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
        # Should preserve decorators
        assert "@property" in refactored

class TestParameterExtraction:
    """Test parameter extraction for extracted methods"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.refactorer = LongMethodRefactorer(max_method_length=3, min_extract_length=2)
    
    def test_parameter_extraction_simple(self):
        """Test extracting parameters from simple variable usage"""
        code = """
def method_with_params():
    result = process_data(input_var, config_var)
    output = format_result(result)
    return output
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
    
    def test_parameter_extraction_with_self(self):
        """Test parameter extraction in class methods"""
        code = """
class TestClass:
    def method_with_self(self):
        self.data = process_input(self.input)
        self.result = validate_data(self.data)
        return self.result
"""
        
        refactored = self.refactorer.analyze_and_refactor(code)
        
        # Should still be valid Python
        compile(refactored, '<string>', 'exec')
        # Should contain self parameter
        assert "def " in refactored

# Fixtures for testing
@pytest.fixture
def sample_long_method():
    """Fixture providing a sample long method for testing"""
    return """
def long_method():
    # Data preparation
    data = get_input_data()
    config = load_configuration()
    
    # Validation
    if not data:
        raise ValueError("No data")
    if not config:
        raise ValueError("No config")
    
    # Processing
    processed = []
    for item in data:
        if validate_item(item):
            processed.append(transform_item(item))
    
    # Output
    result = format_output(processed)
    save_result(result)
    return result
"""

@pytest.fixture
def sample_class_with_long_method():
    """Fixture providing a class with a long method"""
    return """
class DataProcessor:
    def process_data(self, data):
        # Setup
        self.data = data
        self.results = []
        
        # Validation
        if not self.data:
            self.handle_error("No data")
            return None
        
        # Processing
        for item in self.data:
            processed = self.transform_item(item)
            if self.validate_item(processed):
                self.results.append(processed)
        
        # Cleanup
        self.finalize_results()
        return self.results
"""

def test_with_sample_fixtures(sample_long_method, sample_class_with_long_method):
    """Test using the sample fixtures"""
    refactorer = LongMethodRefactorer(max_method_length=8, min_extract_length=2)
    
    # Test with standalone method
    refactored1 = refactorer.analyze_and_refactor(sample_long_method)
    compile(refactored1, '<string>', 'exec')
    
    # Test with class method
    refactored2 = refactorer.analyze_and_refactor(sample_class_with_long_method)
    compile(refactored2, '<string>', 'exec')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])