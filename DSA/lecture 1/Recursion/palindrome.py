def palindrome(i,word):
    if(i>len(word)//2):
        return True
    if(word[i] != word[len(word)-i-1]):
        return False
    return palindrome(i+1,word)

def main():
    word ="naman"
    print(palindrome(0,word))

if __name__=="__main__":
    main()