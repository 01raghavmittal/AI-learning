'''
Given a list of integers, write a function to find the maximum element in the list.


'''

def maximum_element(lst):
    n=len(lst)
    if n == 0:
        return 0
    else:
        max=lst[0]
        for num in lst:
            if num>max:
                max=num
        return max

def maximum_element(lst):
    lst=lst.sort()
    max = lst[-1]
    return max


def maximum_element(lst):
    lst=sorted(lst)
    max = lst[-1]
    return max


def maximum_element(lst):
    return max(lst)



