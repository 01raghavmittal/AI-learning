import math
def prime (n:int=113):
    count=0
    dummy_n=int(math.sqrt(n))

    for i in range(1,dummy_n+1,1):
        if(n%i==0):
            count +=1
            if((n//i)!=i):
                count +=1
    

    if (count==2):
        print('Prime')
    else:
        print('Not Prime')
            

prime()