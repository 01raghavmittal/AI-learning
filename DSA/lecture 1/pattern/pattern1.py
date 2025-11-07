def pattern1(n:int=4):

    '''
    ****
    ****
    ****
    ****
    '''

    for i in range(n):
        
        for j in range(n):
            print('* ',end="")  
        print()  
    return None
pattern1()
print("-"*100)

#-------------------------------------------------------------------------------------------------

def pattern3(n:int=5):
    '''
    1 
    1 2 
    1 2 3 
    1 2 3 4 
    1 2 3 4 5

    '''

    for i in range(n):
        for j in range (i + 1):
            print(j+1,end=" ")
        print()
    return None

pattern3(n=7)

print("-"*100)
#-------------------------------------------------------------------------------------------------

def pattern4(n:int=5):
    '''
    1
    2 2
    3 3 3
    4 4 4 4
    5 5 5 5 5

    '''
    for i in range(n):
        for j in range(i+1):
            print(i+1,end=" ")
        print()
    return None

pattern4()
print("-"*100)

#-------------------------------------------------------------------------------------------------

def pattern5(n:int=4):
    '''
    * * * *
    * * *
    * *
    *
    '''
    for i in range(n):
        for j in range(n,i,-1):
            print('*',end=" ")
        print()

pattern5()
print("-"*100)


#--------------------------------------------------------------------------------------------------

def pattern6(n: int = 5):
    for i in range(n):
        for j in range(1, n - i + 1):
            print(j, end="")
        print()

pattern6()
print("-"*100)


#--------------------------------------------------------------------------------------------------


def pattern7(n: int = 5):
    for i in range(n):
        for j in range(n - i, 0, -1):
            print(j, end="")
        print()

pattern7()
print("-"*100)
