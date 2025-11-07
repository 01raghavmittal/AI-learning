def complex_pattern1(n: int = 5):
    for i in range(n):
        for j in range(n - i - 1):
            print(" ", end="")

        for j in range(2 * i + 1):
            print("*", end="")

        for j in range(n - i - 1):
            print(" ", end="")

        print()


complex_pattern1()

print('-'*100)
def complex_pattern2(n:int=5):

    for i in range(n):
        # space
        for j in range(i):
            print(" ", end="")

        # star
        for j in range(2*n -(2*i +1)):
            print("*", end="")
        
        for j in range(i):
            print(" ", end="")
        
        print()
        # space 

complex_pattern2()


         