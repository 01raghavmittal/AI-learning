def divisor(n:int=36):
    list=[]
    for i in range(1,n+1,1):
        if(n%i==0):
            list.append(i)
    
    print(*list)

divisor()

import math
def all_divisor(n:int=45):
    list=[]
    dummy_n=int(math.sqrt(n))

    for i in range(1,dummy_n+1,1):
        if(n%i==0):
            list.append(i)
            if((n/i)!=i):
                list.append((n//i))
    list.sort()
    print(*list)

all_divisor()
    