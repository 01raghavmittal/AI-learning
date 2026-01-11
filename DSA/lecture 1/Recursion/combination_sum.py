def combination_1(index: int, array: list, target: int, ans: list, result: list):
    # Base case
    if index == len(array):
        if target == 0:
            result.append(ans.copy())
        return

    # Pick the element (can be reused)
    if array[index] <= target:
        ans.append(array[index])
        combination_1(index, array, target - array[index], ans, result)
        ans.pop()  

    # Non pick the element
    combination_1(index + 1, array, target, ans, result)


def combination_sum(array: list, target: int):
    result = []
    combination_1(0, array, target, [], result)
    return result


result=combination_sum(array=[2,3,6,7],target=7)
print(result)
