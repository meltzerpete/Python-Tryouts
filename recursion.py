def countdown(n):
    if n <= 0:
        print("Blastoff!!")
    else:
        print(n)
        countdown(n - 1)

print("Enter a number:")
n = input()
if not isinstance(int(n), int):
    print("Only enter integer!")
countdown(int(n))
