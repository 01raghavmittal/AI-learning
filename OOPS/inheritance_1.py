class User:
    def login(self):
        print("User logged in")
    
    def register(self):
        print("User registered")

class Student(User):

    def attend_class(self):
        print("Student attending class")
    
    def submit_assignment(self):
        print("Student submitted assignment")

Student1 = Student()
Student1.login() # Output: User logged in
Student1.register() # Output: User registered
Student1.attend_class() # Output: Student attending class
Student1.submit_assignment() # Output: Student submitted assignment

