class Function:
    
    def __init__(self, name, body, start_lineno, end_lineno, is_method, belongs_to, closures, complexity, mloc, num_params, num_localvar, branches, long_function=False):
        self.name = name
        self.body = body
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.is_method = is_method
        self.belongs_to = belongs_to
        self.closures = closures
        self.complexity = complexity
        self.mloc = mloc # Lines of code within a function/method (excluding comments and empty lines)
        self.num_params = num_params # Number of function parameters
        self.num_localvar = num_localvar # Number of local variables in the function/method
        self.branches = branches # Number of branches in the function/method (e.g., if, for, while, match)
        self.long_function = long_function

    def get_name(self):

        if self.belongs_to is None:
            return self.name
        else:
            return f"{self.belongs_to}.{self.name}"
        
    def __str__(self):
        return (f"""
    Function: {self.name}
    Body: \n{self.body}
    Start Line: {self.start_lineno}
    End Line: {self.end_lineno}
    Is Method: {self.is_method}
    Belongs to: {self.belongs_to}
    Closures: {self.closures}
    Complexity: {self.complexity}
    Lines of Code: {self.mloc}
    Number of Parameters: {self.num_params}
    Number of Local Variables: {self.num_localvar}
    Branches: {self.branches}
    Long Function: {self.long_function}
    """
        )

    def __repr__(self):
        return (f"""
    Function: {self.name}
    Body:
    {self.body}
    Start Line: {self.start_lineno}
    End Line: {self.end_lineno}
    Is Method: {self.is_method}
    Belongs to: {self.belongs_to}
    Closures: {self.closures}
    Complexity: {self.complexity}
    Lines of Code: {self.mloc}
    Number of Parameters: {self.num_params}
    Number of Local Variables: {self.num_localvar}
    Branches: {self.branches}
    Long Function: {self.long_function}
    """
        )