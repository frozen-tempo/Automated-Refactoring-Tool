import ast
import astor
import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class RefactoringCandidate:
    """Represents a potential refactoring opportunity"""
    method_name: str
    class_name: Optional[str]
    start_line: int
    end_line: int
    lines_of_code: int
    refactoring_type: str
    code_block: List[ast.stmt]
    suggested_name: str
    parameters: List[str]

class LongMethodRefactorer:
    def __init__(self, max_method_length: int = 20, min_extract_length: int = 3):
        self.max_method_length = max_method_length
        self.min_extract_length = min_extract_length
        self.variable_tracker = {}
        
    def analyze_and_refactor(self, source_code: str) -> str:
        """Main entry point for analyzing and refactoring code"""
        tree = ast.parse(source_code)
        candidates = self._find_refactoring_candidates(tree)
        
        if not candidates:
            return source_code
            
        # Apply refactorings
        refactored_tree = self._apply_refactorings(tree, candidates)
        return astor.to_source(refactored_tree)
    
    def _find_refactoring_candidates(self, tree: ast.AST) -> List[RefactoringCandidate]:
        """Find methods that are candidates for refactoring"""
        candidates = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_length = self._count_logical_lines(node)
                
                if method_length > self.max_method_length:
                    class_name = self._find_containing_class(tree, node)
                    
                    # Try different refactoring strategies
                    extract_candidates = self._find_extract_method_candidates(node, class_name)
                    candidates.extend(extract_candidates)
                    
                    # Look for conditional complexity that can be extracted
                    conditional_candidates = self._find_conditional_extraction_candidates(node, class_name)
                    candidates.extend(conditional_candidates)
                    
                    # Look for loop extraction opportunities
                    loop_candidates = self._find_loop_extraction_candidates(node, class_name)
                    candidates.extend(loop_candidates)
        
        return candidates
    
    def _count_logical_lines(self, node: ast.FunctionDef) -> int:
        """Count logical lines of code (excluding comments and blank lines)"""
        lines = set()
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                lines.add(child.lineno)
        return len(lines)
    
    def _find_containing_class(self, tree: ast.AST, method_node: ast.FunctionDef) -> Optional[str]:
        """Find the class containing a method"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if method_node in node.body:
                    return node.name
        return None
    
    def _find_extract_method_candidates(self, method_node: ast.FunctionDef, class_name: Optional[str]) -> List[RefactoringCandidate]:
        """Find consecutive statements that can be extracted into separate methods"""
        candidates = []
        statements = method_node.body
        
        # Look for consecutive statements that form logical groups
        current_group = []
        i = 0
        
        while i < len(statements):
            stmt = statements[i]
            
            # Start a new group
            if not current_group:
                current_group = [stmt]
            else:
                # Check if this statement should be grouped with previous ones
                if self._should_group_statements(current_group[-1], stmt):
                    current_group.append(stmt)
                else:
                    # Process current group if it's large enough
                    if len(current_group) >= self.min_extract_length:
                        candidate = self._create_extract_candidate(
                            current_group, method_node.name, class_name, "extract_method"
                        )
                        if candidate:
                            candidates.append(candidate)
                    
                    # Start new group
                    current_group = [stmt]
            
            i += 1
        
        # Process final group
        if len(current_group) >= self.min_extract_length:
            candidate = self._create_extract_candidate(
                current_group, method_node.name, class_name, "extract_method"
            )
            if candidate:
                candidates.append(candidate)
        
        return candidates
    
    def _find_conditional_extraction_candidates(self, method_node: ast.FunctionDef, class_name: Optional[str]) -> List[RefactoringCandidate]:
        """Find complex conditional blocks that can be extracted"""
        candidates = []
        
        for stmt in ast.walk(method_node):
            if isinstance(stmt, ast.If):
                # Check if the if block is complex enough to extract
                if_lines = self._count_logical_lines_in_block(stmt.body)
                
                if if_lines >= self.min_extract_length:
                    candidate = self._create_extract_candidate(
                        stmt.body, method_node.name, class_name, "extract_conditional"
                    )
                    if candidate:
                        candidate.suggested_name = f"handle_{self._generate_condition_name(stmt.test)}"
                        candidates.append(candidate)
                
                # Check else block
                if stmt.orelse and isinstance(stmt.orelse[0], ast.If):
                    # Handle elif chains
                    continue
                elif stmt.orelse:
                    else_lines = self._count_logical_lines_in_block(stmt.orelse)
                    if else_lines >= self.min_extract_length:
                        candidate = self._create_extract_candidate(
                            stmt.orelse, method_node.name, class_name, "extract_conditional"
                        )
                        if candidate:
                            candidate.suggested_name = f"handle_else_{method_node.name}"
                            candidates.append(candidate)
        
        return candidates
    
    def _find_loop_extraction_candidates(self, method_node: ast.FunctionDef, class_name: Optional[str]) -> List[RefactoringCandidate]:
        """Find loop bodies that can be extracted"""
        candidates = []
        
        for stmt in ast.walk(method_node):
            if isinstance(stmt, (ast.For, ast.While)):
                loop_lines = self._count_logical_lines_in_block(stmt.body)
                
                if loop_lines >= self.min_extract_length:
                    candidate = self._create_extract_candidate(
                        stmt.body, method_node.name, class_name, "extract_loop"
                    )
                    if candidate:
                        if isinstance(stmt, ast.For):
                            candidate.suggested_name = f"process_{self._get_loop_variable_name(stmt)}"
                        else:
                            candidate.suggested_name = f"process_while_loop"
                        candidates.append(candidate)
        
        return candidates
    
    def _should_group_statements(self, stmt1: ast.stmt, stmt2: ast.stmt) -> bool:
        """Determine if two statements should be grouped together"""
        # Group variable assignments
        if isinstance(stmt1, ast.Assign) and isinstance(stmt2, ast.Assign):
            return True
        
        # Group function calls to same object/module
        if isinstance(stmt1, ast.Expr) and isinstance(stmt2, ast.Expr):
            call1 = stmt1.value if isinstance(stmt1.value, ast.Call) else None
            call2 = stmt2.value if isinstance(stmt2.value, ast.Call) else None
            
            if call1 and call2:
                # Check if calls are to the same object/module
                func1_name = self._get_function_name(call1)
                func2_name = self._get_function_name(call2)
                
                if func1_name and func2_name:
                    # Group calls to same module/object
                    return func1_name.split('.')[0] == func2_name.split('.')[0]
        
        return False
    
    def _create_extract_candidate(self, statements: List[ast.stmt], method_name: str, 
                                class_name: Optional[str], refactoring_type: str) -> Optional[RefactoringCandidate]:
        """Create a refactoring candidate from a group of statements"""
        if not statements:
            return None
        
        # Analyze variable usage to determine parameters
        used_vars = self._analyze_variable_usage(statements)
        
        # Generate suggested method name
        suggested_name = self._generate_method_name(statements, method_name, refactoring_type)
        
        return RefactoringCandidate(
            method_name=method_name,
            class_name=class_name,
            start_line=statements[0].lineno,
            end_line=statements[-1].lineno,
            lines_of_code=len(statements),
            refactoring_type=refactoring_type,
            code_block=statements,
            suggested_name=suggested_name,
            parameters=list(used_vars)
        )
    
    def _analyze_variable_usage(self, statements: List[ast.stmt]) -> Set[str]:
        """Analyze which variables are used in the statements and need to be parameters"""
        used_vars = set()
        defined_vars = set()
        
        for stmt in statements:
            # Find variables that are used (read)
            for node in ast.walk(stmt):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id not in defined_vars:
                        used_vars.add(node.id)
                
                # Track variables that are defined in this block
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    defined_vars.add(node.id)
        
        # Filter out built-in names and common Python keywords
        builtin_names = {'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip'}
        used_vars = {var for var in used_vars if var not in builtin_names and not var.startswith('_')}
        
        return used_vars
    
    def _generate_method_name(self, statements: List[ast.stmt], original_method: str, refactoring_type: str) -> str:
        """Generate a meaningful name for the extracted method"""
        # Try to infer purpose from the statements
        action_words = []
        
        for stmt in statements:
            if isinstance(stmt, ast.Assign):
                action_words.append("set")
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = self._get_function_name(stmt.value)
                if func_name:
                    action_words.append(func_name.split('.')[-1])
            elif isinstance(stmt, ast.If):
                action_words.append("check")
            elif isinstance(stmt, (ast.For, ast.While)):
                action_words.append("process")
        
        if action_words:
            primary_action = action_words[0]
            return f"{primary_action}_{refactoring_type.split('_')[1]}"
        
        return f"extracted_from_{original_method}"
    
    def _get_function_name(self, call_node: ast.Call) -> Optional[str]:
        """Extract function name from a call node"""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return None
    
    def _generate_condition_name(self, condition: ast.expr) -> str:
        """Generate a meaningful name from a condition"""
        if isinstance(condition, ast.Compare):
            if isinstance(condition.left, ast.Name):
                return condition.left.id
        elif isinstance(condition, ast.Name):
            return condition.id
        return "condition"
    
    def _get_loop_variable_name(self, loop_node: ast.For) -> str:
        """Get the loop variable name"""
        if isinstance(loop_node.target, ast.Name):
            return loop_node.target.id
        return "item"
    
    def _count_logical_lines_in_block(self, block: List[ast.stmt]) -> int:
        """Count logical lines in a block of statements"""
        lines = set()
        for stmt in block:
            for node in ast.walk(stmt):
                if hasattr(node, 'lineno'):
                    lines.add(node.lineno)
        return len(lines)
    
    def _apply_refactorings(self, tree: ast.AST, candidates: List[RefactoringCandidate]) -> ast.AST:
        """Apply the identified refactorings to the AST"""
        # Create a transformer that will modify the AST
        transformer = RefactoringTransformer(candidates)
        return transformer.visit(tree)

class RefactoringTransformer(ast.NodeTransformer):
    def __init__(self, candidates: List[RefactoringCandidate]):
        self.candidates = candidates
        self.new_methods = []
        self.processed_methods = set()
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Transform function definitions"""
        # Find candidates for this method
        method_candidates = [c for c in self.candidates if c.method_name == node.name]
        
        if not method_candidates:
            return self.generic_visit(node)
        
        # Apply refactorings
        new_body = []
        original_body = node.body[:]
        i = 0
        
        while i < len(original_body):
            stmt = original_body[i]
            
            # Check if this statement is part of a refactoring candidate
            candidate = self._find_candidate_for_statement(stmt, method_candidates)
            
            if candidate and candidate.method_name not in self.processed_methods:
                # Replace the block with a method call
                method_call = self._create_method_call(candidate)
                new_body.append(method_call)
                
                # Create the new method
                new_method = self._create_extracted_method(candidate)
                self.new_methods.append(new_method)
                
                # Skip the statements that were extracted
                i += len(candidate.code_block)
                self.processed_methods.add(f"{candidate.method_name}_{candidate.suggested_name}")
            else:
                new_body.append(stmt)
                i += 1
        
        # Update the method body
        node.body = new_body
        return node
    
    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Transform class definitions to add new methods"""
        # Visit the class normally first
        node = self.generic_visit(node)
        
        # Add any new methods that were created
        node.body.extend(self.new_methods)
        self.new_methods = []  # Clear for next class
        
        return node
    
    def _find_candidate_for_statement(self, stmt: ast.stmt, candidates: List[RefactoringCandidate]) -> Optional[RefactoringCandidate]:
        """Find if a statement is part of a refactoring candidate"""
        for candidate in candidates:
            if stmt in candidate.code_block:
                return candidate
        return None
    
    def _create_method_call(self, candidate: RefactoringCandidate) -> ast.stmt:
        """Create a method call statement to replace the extracted code"""
        # Create the call
        if candidate.class_name:
            call = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='self', ctx=ast.Load()),
                    attr=candidate.suggested_name,
                    ctx=ast.Load()
                ),
                args=[ast.Name(id=param, ctx=ast.Load()) for param in candidate.parameters],
                keywords=[]
            )
        else:
            call = ast.Call(
                func=ast.Name(id=candidate.suggested_name, ctx=ast.Load()),
                args=[ast.Name(id=param, ctx=ast.Load()) for param in candidate.parameters],
                keywords=[]
            )
        
        return ast.Expr(value=call)
    
    def _create_extracted_method(self, candidate: RefactoringCandidate) -> ast.FunctionDef:
        """Create a new method from the extracted code"""
        # Create parameters
        args = [ast.arg(arg=param, annotation=None) for param in candidate.parameters]
        
        # Add self parameter if it's a class method
        if candidate.class_name:
            args.insert(0, ast.arg(arg='self', annotation=None))
        
        # Create the new method
        new_method = ast.FunctionDef(
            name=candidate.suggested_name,
            args=ast.arguments(
                posonlyargs=[],
                args=args,
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=candidate.code_block[:],  # Copy the statements
            decorator_list=[],
            returns=None,
            type_comment=None
        )
        
        return new_method

# Example usage and testing
def demo_refactoring():
    """Demonstrate the refactoring tool"""
    sample_code = '''
class DataProcessor:
    def process_data(self, data, config):
        # Validation section
        if not data:
            raise ValueError("Data cannot be empty")
        if not config:
            raise ValueError("Config cannot be empty")
        
        # Data cleaning section
        cleaned_data = []
        for item in data:
            if item is not None:
                cleaned_item = str(item).strip()
                if cleaned_item:
                    cleaned_data.append(cleaned_item)
        
        # Configuration setup
        max_items = config.get('max_items', 100)
        min_length = config.get('min_length', 1)
        output_format = config.get('format', 'json')
        
        # Data processing
        processed_data = []
        for item in cleaned_data:
            if len(item) >= min_length:
                processed_item = item.upper()
                processed_data.append(processed_item)
                if len(processed_data) >= max_items:
                    break
        
        # Output formatting
        if output_format == 'json':
            import json
            result = json.dumps(processed_data)
        elif output_format == 'csv':
            result = ','.join(processed_data)
        else:
            result = str(processed_data)
        
        return result
'''
    
    refactorer = LongMethodRefactorer(max_method_length=10, min_extract_length=3)
    refactored_code = refactorer.analyze_and_refactor(sample_code)
    
    print("Original code:")
    print(sample_code)
    print("\nRefactored code:")
    print(refactored_code)

if __name__ == "__main__":
    demo_refactoring()