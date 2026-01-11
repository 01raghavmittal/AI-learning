def distint_element(array: list, k: int):
    result = []
    window = []

    # first window
    for i in range(k):
        window.append(array[i])

    result.append(len(set(window)))

    # slide the window
    for i in range(k, len(array)):
        window.pop(0)          # remove outgoing element
        window.append(array[i]) # add incoming element
        result.append(len(set(window)))

    return result
