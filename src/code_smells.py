import math

from math import *

global greeting

def open_file_bad():
    file = open('code_smells.py', 'r')
    code = file.read()
    print(code)
    
def open_file_good():
    with open ('code_smells.py','r') as file:
        code = file.read()
        print(code)

def bad_bool():
    var = True
    if var == True:
        print("Greeting")

def good_bool():
    var = True
    if var:
        print("Hello")

