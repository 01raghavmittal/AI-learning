class Atm:
    
    def __init__(self):
        self.__pin = ""
        self.__balance = 0
    
    def get_balance(self):
        return self.__balance

sbi = Atm()

sbi.__balance="qwerty"

amount = sbi.get_balance()
print(amount) # 0

sbi._Atm__balance="qwerty"
amount = sbi.get_balance()
print(amount) # qwerty 




'''


Your code runs into an **error because of private variables**.

---

### ❌ Problem:

```python
amount = sbi.__balance
```

This will give:

```
AttributeError: 'Atm' object has no attribute '__balance'
```

---

### 🔍 Why this happens:

In Python, variables with **double underscores (`__`)** are *name-mangled* to make them private.

So inside your class:

```python
self.__balance
```

actually becomes:

```python
self._Atm__balance
```

This means you **cannot access it directly** like `sbi.__balance` from outside the class.

---

### ✅ Correct ways to access it:

#### ✔️ 1. Use a getter method (best practice)

```python
class Atm:
    
    def __init__(self):
        self.__pin = ""
        self.__balance = 0
    
    def get_balance(self):
        return self.__balance

sbi = Atm()
amount = sbi.get_balance()
print(amount)
```

---

#### ✔️ 2. (Not recommended) Access using name mangling

```python
print(sbi._Atm__balance)
```

This works, but **breaks encapsulation** and should be avoided.

---

### 💡 Key idea:

* `__variable` → private (name-mangled)
* Access it via methods → **good OOP practice**

---

If you want, I can show how to build a simple ATM system with deposit/withdraw functions 👍

'''