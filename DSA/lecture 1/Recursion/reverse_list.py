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


def reverse_1(i,list):
    if(i>=len(list)//2):
        return list
    list[i],list[len(list)-i-1]=list[len(list)-i-1],list[i]
    return reverse_1(i+1,list)






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

    print("Reverse list method 2: ",reverse_1(0, list))

    

    


if __name__=="__main__":
    main()