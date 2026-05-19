class Customer:
    def __init__(self, name, gender, address):
        self.name = name
        self.gender = gender
        self.address = address
    def edit_customer(self,new_name,new_city,new_state):
        self.name = new_name
        self.address.edit_address(new_city, new_state)

class Address:
    def __init__(self, city, state):
        self.city = city
        self.state = state 

    def edit_address(self, new_city, new_state): 
        self.city = new_city
        self.state = new_state




add= Address("New York", "NY")
Cust=Customer("John Doe", "Male", add)

print(Cust.address) # Output: <__main__.Address object at 0x7f8b8c2e5d30>
print(Cust.address.city) # Output: New York
print(Cust.address.state) # Output: NY


#------------------------------------------------------

Cust.edit_customer("Raghav", "Los Angeles", "CA")

print(Cust.address.city) # Output: Los Angeles
print(Cust.address.state) # Output: CA







