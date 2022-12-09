import numpy as np
import math

def add(x,y=0):
    return x+y
def sub(x,y=0):
    return x-y
def mul(x, y=0):
    return x*y
def division(x, y=1):
    return x/y
def square(x,y=0):
    return (x+y)**2
def square_root(x,y=0):
    return abs(x+y)**(1/2)
def cube(x,y=0):
    return (x + y) ** 3
def  protected(x, y=1):
    if y != 0:
        z=x / y
    else:
        z=1
    return z
def cal_max(x,y=0):
    return max(x, y)
def cal_min(x,y=0):
    return min(x, y)
def sin(x,y=1):
    y=1
    return math.sin(x*y)
def cos(x,y=1):
    y = 1
    return math.cos(x*y)
FUNCTIONS =[add,sub,mul,division,square,square_root,cube,protected,cal_max,cal_min,sin,cos]