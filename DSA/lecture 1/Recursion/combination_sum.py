def combination_sum(arr, index, target, dummy_list, answer):
    # Base case: if we reach the end of the array
    if index == len(arr):
        if target == 0:
            # Add a copy of the current combination to the answer
            answer.append(dummy_list[:])
        return
    
    # If current element can be included
    if arr[index] <= target:
        # Include the element
        dummy_list.append(arr[index])
        # Recurse with same index (since we can reuse the element)
        combination_sum(arr, index, target - arr[index], dummy_list, answer)
        # Backtrack (remove the element)
        dummy_list.pop()
    
    # Move to the next index
    combination_sum(arr, index + 1, target, dummy_list, answer)


# Example usage
arr = [2, 3, 6, 7]
target = 7
answer = []
combination_sum(arr, 0, target, [], answer)
print("Combinations that sum to target:", answer)
