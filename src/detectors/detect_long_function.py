class LongFunctionDetector:

    def __init__(self):
        self.long_functions = []

    def check_long_function(self, functions):

        for func in functions:
            if (func.mloc > 50) or (func.complexity > 5) or (((func.num_params > 5) or (func.num_localvar > 10)) and func.branches > 4):
                func.long_function = True
                self.long_functions.append(
                {
                    "name": func.name,
                    "start_lineno":func.start_lineno,
                    "end_lineno": func.end_lineno,
                    "is_method": func.is_method,
                    "belongs_to": func.belongs_to,
                    "closures": func.closures,
                    "complexity": func.complexity,
                    "mloc": func.mloc,
                    "num_params": func.num_params,
                    "num_localvar": func.num_localvar,
                    "branches": func.branches,
                    "long_function": func.long_function
                })
            