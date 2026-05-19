"""



"""

class Atm :

    def __init__(self):
        self.pin =""
        self.balance = 0

        self.menu()

    def menu(self):

        user_input =  input(""" 
                    Hello, How would you like to proceed

                    1. Enter '1' to create pin
                    2. Enter '2' to deposit
                    3. Enter '3' to withdraw
                    4. Enter '4' to check balance
                    5. Enter '5' to Exit
                     """)
        if user_input == '1':
            self.create_pin()
        elif user_input == '2':
            print()
        elif user_input == '3':
            print()
        elif user_input == '4':
            print()
        elif user_input == '5':
            print()
        else:
            print("Invalid Message ... please try again")
        
    
    def create_pin(self):
        if self.pin =="":
            new_pin = input("Please Enter your pin ")
            self.pin=str(new_pin)
        else:
            old_pin= input("Please Enter your Old pin")
            if(str(old_pin)==self.pin):
                new_pin = input("Please Enter your pin")
                self.pin=str(new_pin)
            else:
                print("Wrong Pin")
    
    def deposit(self):
        





    



    







#===========MAIN====================

if __name__ == "__main__":
    atm = Atm()