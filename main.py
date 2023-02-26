"""
CMPS 2200  Recitation 3.
See recitation-03.pdf for details.
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    
## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.

def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def quadratic_multiply(x, y):
    # 1. obtian binary values of x and y calling them xvec and yvec
    xvec = x.binary_vec
    yvec = y.binary_vec
    
    # 2. pad xvec and yvec so lengths are equal for proper splitting and recombination
    xvec, yvec = pad(xvec, yvec)

    # 3. base case returning product of x and y if both <=1
    if x.decimal_val <=1 and y.decimal_val <=1:
        return BinaryNumber(x.decimal_val*y.decimal_val)

    # 4. split xvec and yvec into two halves
    x_left, x_right = split_number(xvec)
    y_left, y_right = split_number(yvec)

    # 5. implement apply quadratic multiply formula
    # formula:
    # left = 2^n * x_left * y_left
    # mid = 2^(n /2) * (x_left * y_right + x_right * y_left)
    # right = x_right * y_right

    left = quadratic_multiply(x_left, y_left)
    mid_left = quadratic_multiply(x_left, y_right)
    mid_right = quadratic_multiply(x_right, y_left)

    mid = BinaryNumber(mid_left.decimal_val + mid_right.decimal_val)

    # 6. use bitshift for 2^n and 2^(n/2) multiplications
    mid = bit_shift(mid, len(xvec)//2) 
    left = bit_shift(left, len(xvec))
    right = quadratic_multiply(x_right, y_right)

    # 7. sum the 3 decimal values for final answer to return
    return BinaryNumber(left.decimal_val + mid.decimal_val + right.decimal_val)

## Feel free to add your own tests here.
def test_multiply():
    assert quadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2*2
    
    # added tests fully functional
    assert quadratic_multiply(BinaryNumber(4), BinaryNumber(6)).decimal_val == 4*6
    assert quadratic_multiply(BinaryNumber(2), BinaryNumber(7)).decimal_val == 2*7
    
def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    return (time.time() - start)*1000

test_multiply()