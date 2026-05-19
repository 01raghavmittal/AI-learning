print("Inheritance example")
print("-"*50)
print()
print()
print("="*50)
print("Example 1 : Inheriting constructor")
print("="*50)

class Phone:
    def __init__(self, brand, model):
        print("Phone constructor called")
        self.brand = brand
        self.model = model
    def buy(self):
        print(f"Buying {self.brand} {self.model}")
    
    def rturn_phone(self):
        print(f"Returning {self.brand} {self.model}")

class FeaturePhone(Phone):
    pass

class SmartPhone(Phone):
    pass

mobile1 = SmartPhone("Apple", "iPhone 14")

#-----------------------------------------------------------------------------------------------------------------------------------------------------

print()
print()
print("="*50)
print("Example  2: Inheriting private attributes")
print("="*50)

class Customer:
    def __init__(self, name, gender,worth):
        self.name = name
        self.gender = gender
        self.__worth = worth # private attribute
    def get_name(self):
        return self.name
    def get_gender(self):
        return self.gender
    def get_customer_worth(self):
        return self.__worth

class VIPCustomer(Customer):
    def get_worth(self):
        return self.__worth

vip1 = VIPCustomer("Alice", "Female", 1000000)
print(vip1.get_name()) # Output: Alice  
print(vip1.get_gender()) # Output: Female
print(vip1.get_customer_worth()) # Output: 1000000
# print(Customer.__worth) # Output: Customer' object has no attribute '__worth' because __worth is a private attribute and cannot be accessed directly from outside the class or can't be
# print(vip1.get_worth()) # Output: VIPCustomer' object has no attribute '_VIPCustomer__worth'



# results in an error because __worth is a private attribute and cannot be accessed directly from outside the class or can't be inherited directly.

#-----------------------------------------------------------------------------------------------------------------------------------------------------


print()
print()
print("="*50)
print("Example  3: polymorphism ")
print("="*50)

class Phone:
    def __init__(self, brand, price):
        print("Phone constructor called")
        self.__price = price
        self.brand = brand
    
    def buy(self):
        print(f"Phone class :Buying {self.brand} phone for {self.__price}")

    def return_phone(self):
        print(f"Phone class :Returning {self.brand} phone")

class FeaturePhone(Phone):
    
    def buy(self):
        print(f"FeaturePhone class :Buying {self.brand} feature phone for {self._Phone__price}")

class SmartPhone(FeaturePhone):
    def buy(self):
        print(f"SmartPhone class :Buying {self.brand} smartphone for {self._Phone__price}")


mobile1 = SmartPhone("Apple", 999)
mobile1.buy() # Output: SmartPhone class :Buying Apple smartphone for 999

#-----------------------------------------------------------------------------------------------------------------------------------------------------


print()
print()
print("="*50)
print("Example  4: problem with private attributes in inheritance ")
print("="*50)
print()


class Parent:
    def __init__(self, num):
        self.__num = num

    def get_num(self):
        return self.__num

class Child(Parent):
    def __init__(self, val,num):
        self.__val = val
        super().__init__(num)
    
    def get_val(self):
        return self.__val

son=Child(10,20) # this line 
print(son.get_num()) # Output: 20
print(son.get_val()) # Output: 10


#-----------------------------------------------------------------------------------------------------------------------------------------------------


print()
print()
print("="*50)
print("Example  5: problem with Arguments in inheritance ")
print("="*50)



class A:
    def __init__(self):
        self.num = 10
    def display(self,num):
        print(f"Value of num in class A: {self.num}")

class B(A):
    def display2(self,num):
        print(f"Value of num in class B: {self.num}")

objectB = B()
objectB.display(20) # Output: Value of num in class A: 10
objectB.display2(30) # Output: Value of num in class B: 10


#-----------------------------------------------------------------------------------------------------------------------------------------------------


print()
print()
print()
print("="*50)
print("Example  6: Super keyword in inheritance ")
print("="*50)


class Phone:
    def __init__(self, brand, price):
        print("Phone constructor called")
        self.__price = price
        self.brand = brand
    
    def buy(self):
        print(f"Phone class :Buying {self.brand} phone for {self.__price}")

class SmartPhone(Phone):
    def __init__(self, brand, price):
        super().__init__(brand, price)
        
    
    def buy(self):
        print(f"SmartPhone class :Buying {self.brand} smartphone for {self._Phone__price}")
        super().buy()

mobile1 = SmartPhone("Apple", 999)
mobile1.buy()

#-----------------------------------------------------------------------------------------------------------------------------------------------------
