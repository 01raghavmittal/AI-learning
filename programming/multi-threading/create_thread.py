import threading 
import time

def thread_fun(name):
    print(f"thread fucntion is starting for {name}")
    print(f"[{name}] Thread ID: {threading.get_ident()}") # Returns a unique  numeric ID of the current thread
    print(f"[{name}] Thread object:{threading.current_thread()}") # Returns a unique Thread object of the current thread
    time.sleep(5)
    print(f"thread function is completed for {name}")


print(f"🔹 Threads after creating (before start): {threading.active_count()}") # threading.active_count() it will give me how many thread in python script is running 


task1=threading.Thread(target=thread_fun, args=("A",))
print(f"task1 thread identity is {task1.ident}")
task2=threading.Thread(target=thread_fun, args=("B",))
task3=threading.Thread(target=thread_fun, args=("C",))


task1.start()
print(f"task1 thread identity is {task1.ident}")
task2.start()
task3.start()

print(f"🔹 Threads while running: {threading.active_count()}")
print('*'*50)
print(threading.enumerate()) # Returns a list of all currently active Thread objects
print('*'*50)
print(threading.main_thread()) # Returns the main Thread object

# Wait for both to finish
task1.join()
task2.join()
task3.join()

# ✅ After all threads finish
print(f"🔹 Threads after completion: {threading.active_count()}")




'''
threading.active_count() --> Count active number of threads that are running 

threading.get_ident() --> Give a unique ramdom thread ID that is assign ramdomly by kernel of current thread

threading.current_thread() --> Give a object of current thread 

threading.enumerate() --> Give me a list of all currently active Thread objects

threading.main_thread() --> Give me a Object of Main thread 

'''
