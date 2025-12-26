def reverse_number(n=-321):
    rev_num=0
    sign= -1 if n<0 else 1
    n=abs(n)
    while(n>0):
        last_digit=n%10
        n=n//10
        rev_num=(rev_num*10)+last_digit
    rev_num=sign*rev_num
    print(rev_num)
    

reverse_number()