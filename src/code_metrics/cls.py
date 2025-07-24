class Class:

    def __init__(self, name, start_lineno, end_lineno, methods, complexity,mloc):
        self.name = name
        self.start_lineno = start_lineno
        self.end_lineno = end_lineno
        self.methods = methods
        self.complexity = complexity
        self.mloc = mloc

    def avg_method_complexity(self):
        return sum(methd.complexity for methd in self.methods) / len(self.methods)

    def __str__(self):
        return f"Class:{self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Class Body Length: {self.mloc} \n Methods: {self.methods} \n Complexity: {self.complexity} \n Avg Complexity: {self.avg_method_complexity()}"
    
    def __repr__(self):
        return f"Class:({self.name} \n Start Line: {self.start_lineno} \n End Line: {self.end_lineno} \n Class Body Length: {self.mloc} \n Methods: \n {self.methods} \n Complexity: {self.complexity} \n Avg Complexity: {self.avg_method_complexity()})"
   
    def get_method_loc(self):
        return sum(method.mloc for method in self.methods)
