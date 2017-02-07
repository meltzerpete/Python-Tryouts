def add_all(t):
    total = 0
    for x in t:
        total += x
    return total

print(add_all([3,2,3,4,5,3]))

def capitalize_all(t):
    res = []
    for s in t:
        res.append(s.capitalize())
    return res

print(capitalize_all("hello"))
