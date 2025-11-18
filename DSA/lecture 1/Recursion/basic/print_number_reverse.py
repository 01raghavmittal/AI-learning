def number_rev(n):
    if(n==0):
        return 
    print(n)
    number_rev(n-1)

        
def main():
    n=int(input())
    print('*'*100)
    number_rev(n)



if __name__ == "__main__":
    main()