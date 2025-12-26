# brute
def gcd(a=20,b=40):
    gcd=0
    for i in range(1,min(a,b)+1,1):
        if(a%i==0 & b%i==0):
            gcd=i
    print (gcd)

gcd()
print('*'*100)


def hcf(a=20,b=40):
    while(a>0 and b>0):
        if(a>b):
            a=a%b
        else:
            b=b%a

    if(a==0):
        print(b)
    else:
        print(a)

hcf()    



