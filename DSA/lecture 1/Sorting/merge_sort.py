def MergeSort(arr):
    merge_Sort(arr, 0, len(arr) - 1)

def merge(arr, low,mid, high):
    left=low
    right=mid+1
    temp=[]
    while left<=mid and right<=high:
        if arr[left]<=arr[right]:
            temp.append(arr[left])
            left+=1
        else:
            temp.append(arr[right])
            right+=1
    while left<=mid:
        temp.append(arr[left])
        left+=1
    while right<=high:
        temp.append(arr[right])
        right+=1
    for i in range(len(temp)):
        arr[low+i]=temp[i]


def merge_Sort(arr, low, high):
    if low==high:
        return
    mid = (low + high) // 2
    merge_Sort(arr, low, mid)
    merge_Sort(arr, mid + 1, high)
    merge(arr, low, mid, high)




def main():
    arr = [38, 27, 43, 3, 9, 3, 82, 10]

    MergeSort(arr)
    print(arr)


if __name__ == "__main__":
    main()