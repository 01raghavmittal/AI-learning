def main():
    n=int(input())
    sum_n(n,sum=0)
    print(sum_n2(n))



def sum_n(i,sum):
    if(i<0):
        print(sum)
        return
    sum_n(i-1,sum+i)


def sum_n2(i):
    if(i==0):
        return 0
    return i + sum_n2(i-1)





if __name__ == "__main__":
    main()