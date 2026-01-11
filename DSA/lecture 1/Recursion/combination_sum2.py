from typing import List
def combinationSum2( candidates: List[int], target: int) -> List[List[int]]:
    result=[]
    candidates.sort()
    combination(index=0,array=candidates,target=target,d_list=[],ans=result)

    return result

def combination(index,array,target,d_list,ans):
    if target==0:
        ans.append(d_list.copy())
        return
    
    for i in range(index,len(array),1):
        if(i>index and array[i]==array[i-1]):
            continue
        if array[i]>target:
            break
        d_list.append(array[i])
        combination(i+1,array,target-array[i],d_list,ans)
        d_list.pop()
        



     