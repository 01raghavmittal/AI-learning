def palindrome(n=101):
    dummy_n=n
    rev_num=0
    while(n>0):
        last_digit=n%10
        n=n//10
        rev_num=(rev_num*10)+last_digit

    if (rev_num==dummy_n):
        print("True")
    else:
        print("False")  
    

palindrome()