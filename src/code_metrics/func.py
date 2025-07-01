class Function:
    
    def __init__(self, name, start_lineno, end_lineno, is_method, belongs_to, closures, complexity):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.is_method = is_method
        self.belongs_to = belongs_to
        self.closures = closures
        self.complexity = complexity
        self.halstead_vocab = 0
        self.halstead_length = 0
        self.halstead_estimated_length = 0
        self.halstead_volume = 0
        self.halstead_difficulty = 0
        self.halstead_effort = 0

    def get_name(self):

        if self.belongs_to is None:
            return self.name
        else:
            return f"{self.belongs_to}.{self.name}"
        
    def __str__(self):
        return f"Function: {self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Belongs to: {self.belongs_to} \n Complexity: {self.complexity}"

    def __repr__(self):
        return f"Function: ({self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Belongs to: {self.belongs_to} \n Complexity: {self.complexity} \n)"