def main():
    n = int(input())
    name(1, n)  

def name(i, n):
    if i > n:
        return
    print("Name")
    name(i + 1, n)   

if __name__ == "__main__":
    main()
