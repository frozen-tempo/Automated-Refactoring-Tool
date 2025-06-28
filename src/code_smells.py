def simple_function():

    def other_simple_function(x):
        print(x)
    
    return other_simple_function

for i in range(10):
    print(i)

class SimpleClass:
    def method(self):
        return "Hello, World!"

    def another_method(self, x):
        if x > 10:
            return x * 2