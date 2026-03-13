def fun(arr, index, current_sum, answer):
    # Base case: if we've considered all elements
    if index == len(arr):
        answer.append(current_sum)
        print(answer)
        return
    
    # Include current element
    fun(arr, index + 1, current_sum + arr[index], answer)
    
    # Exclude current element
    fun(arr, index + 1, current_sum, answer)


# Example usage
arr = [3, 1, 2]
answer = []
fun(arr, 0, 0, answer)
answer.sort() 
print(*answer)
