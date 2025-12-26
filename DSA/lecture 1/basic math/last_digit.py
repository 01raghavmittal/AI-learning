def last_digit(n=1089):
    while(n>0):
        last_digit=n%10
        n=n//10
        print(last_digit)
    return None

last_digit()