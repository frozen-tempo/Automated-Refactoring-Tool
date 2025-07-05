class cls:

    def __init__(self) -> None:
        self.x = 10

cls_1 = cls()

def func():
    y = 1
    z = y + return_x()
    cls_1.x = 20
    return z
    
def return_x():
    x = 5
    return x

print(cls_1.x)
func()
print (cls_1.x)