def sqrt(n):
    return xsqrt(n, 1)

def xsqrt(n, x):
    y = (x + n/x) / 2
    if abs(y - x) < 0.00000000000001:
        return y
    else:
        return xsqrt(n, y)

n = input("Enter number: ")
print(sqrt(float(n)))
