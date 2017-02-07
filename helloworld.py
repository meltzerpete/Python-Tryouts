
import math
print ("hello world!!");
a = 0
a += 2
print (a)
print(math.pi)

def my_func(words):
    print("pete says " + words)

    def my_inner_func():
        print("blah")

    my_inner_func()

my_func("yo!")
my_inner_func()
