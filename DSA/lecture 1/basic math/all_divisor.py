def divisor(n:int=36):
    list=[]
    for i in range(1,n+1,1):
        if(n%i==0):
            list.append(i)
    