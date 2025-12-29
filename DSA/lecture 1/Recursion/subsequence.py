def subsequence(index,dummy_list,list):
    if(index==len(list)):
        print(dummy_list)
        return
    dummy_list.append(list[index])
    subsequence(index+1,dummy_list,list)
    dummy_list.pop()
    subsequence(index+1,dummy_list, list)


def main():
    list=[1,2,3]
    subsequence(index=0,dummy_list=[],list=list)

if __name__=="__main__":
    main()