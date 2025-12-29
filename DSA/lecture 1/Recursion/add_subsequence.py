def add_subsequence(index, dummy_list, arr, total, target):
    if index == len(arr):
        if total == target:
            print(dummy_list)
        return  

    dummy_list.append(arr[index])
    add_subsequence(index + 1, dummy_list, arr, total + arr[index], target)
    # total=total-arr[index]

    dummy_list.pop()

    add_subsequence(index + 1, dummy_list, arr, total, target)


def main():
    arr = [1, 2, 1]
    add_subsequence(index=0, dummy_list=[], arr=arr, total=0, target=2)


if __name__ == "__main__":
    main()
