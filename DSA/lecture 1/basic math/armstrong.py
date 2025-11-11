def armstrong(n=371):
    sum=0
    dummy_n=n
    while(n>0):
        last_digit=n%10
        n=n//10
        sum=(last_digit*last_digit*last_digit)+sum
    if(sum==dummy_n):
        return True
    else:
        return False

print(armstrong(371))
