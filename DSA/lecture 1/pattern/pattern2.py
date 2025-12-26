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
            print('*', end="")
        
        for j in range(i):
            print(" ", end="")
        
        print()
        # space 

complex_pattern2()
print('-'*100)

#---------------------------------------------------------------------
def complex_pattern3(n:int=5):
    complex_pattern1(n)
    complex_pattern2(n)

complex_pattern3()
print('-'*100)      

#---------------------------------------------------------------------


def complex_pattern4(n: int = 5):
    for i in range(1, 2 * n):  
        value = i
        if i > n:
            value = 2 * n - i  # Decreasing part after midpoint
        for j in range(value):  
            print('*', end=' ')
        print()
    return None



complex_pattern4()
print('-'*100)   


#---------------------------------------------------------------------


def complex_pattern5(n:int =5):
    for i in range(n):
        if(i%2==0):
            start =0
        else:
            start=1
        for j in range(i+1):
            print(start,end=" ")
            start=1-start
        print()
    return None  

complex_pattern5()
print('-'*100)  


#---------------------------------------------------------------------

def complex_pattern6(n:int=5):
    for i in range(n):
        # numbers 
        for j in range (i+1):
            print(j+1,end="")

        space=2*n-2*(i+1)
        for j in range(space):
            print(" ",end="")
        
        
        for j in range(i + 1, 0, -1):
            print(j,end="")
         
        print()
    return None 



complex_pattern6()
print('-'*100)  




#---------------------------------------------------------------------

def complex_pattern7(n:int=5):
    start=1
    for i in range(1,n+1,1):
        for j in range(1,i+1,1):
            print(start,end=" ")
            start=start+1
        print()
    return None

complex_pattern7()
print('-'*100)  



#---------------------------------------------------------------------
