def reverse(l,r,list):
    if not (l>=r):
        if(list[l]==list[r]):
            l+=1
            r-=1
            rev_list=reverse(l,r,list)
            return rev_list
        else:
            list[l],list[r]=list[r],list[l]
            l+=1
            r-=1
            rev_list=reverse(l,r,list)
            return rev_list
    else:
        return list




def main():
    n=int(input())
    list=[]
    for i in range(n):
        list.append(int(input()))

    print("list is ",list)
    l=0
    r=n-1
    rev_list=reverse(l,r,list)
    print("reverse list is ",rev_list)

    

    


if __name__=="__main__":
    main()