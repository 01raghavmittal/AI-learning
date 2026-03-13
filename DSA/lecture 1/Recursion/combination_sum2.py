def fun(arr, index, target, dummy_list, answer):
    # Base case: target reached
    if target == 0:
        answer.append(list(dummy_list))  # store a copy of current combination
        return

    for i in range(index, len(arr)):
        # Skip duplicates
        if i > index and arr[i] == arr[i-1]:
            continue

        # If current number exceeds target, stop exploring further
        if arr[i] > target:
            break

        # Choose the current number
        dummy_list.append(arr[i])

        # Recurse with reduced target and next index
        fun(arr, i+1, target - arr[i], dummy_list, answer)

        # Backtrack (remove last chosen number)
        dummy_list.pop()

arr = [10, 1, 2, 7, 6, 1, 5]
target = 8

# Sort array to handle duplicates properly
arr.sort()

answer = []
fun(arr, 0, target, [], answer)

print("Combinations that sum to", target, ":")
print(answer)
