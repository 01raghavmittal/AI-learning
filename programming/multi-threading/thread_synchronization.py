import threading
import time

lock = threading.Lock()

def worker(name):
    print(f"{name} trying to acquire lock...")
    with lock:
        print(f"{name} acquired lock ✅")
        time.sleep(3)  # Simulate some long work
        print(f"{name} releasing lock 🔓")

t1 = threading.Thread(target=worker, args=("Thread-1",))
t2 = threading.Thread(target=worker, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("All threads done!")


#--------------------------------------------------------------------------------------------------------
print("*"*100)
'''
You have:

Two threads (Task 1, Task 2)

Both call an API

There’s a Lock protecting the critical section (maybe around the API call or data writing)

Task 1 gets an error while holding the lock

You’re asking:

❓ “If Task 1 throws an error, will Task 2 still execute — or get stuck waiting forever?”



✅ Short Answer

It depends how you use the Lock:

Case	Will Task 2 execute after Task 1 fails?
If you use with lock:	✅ Yes, Task 2 executes (lock auto-released even on error)
If you use lock.acquire() but forget lock.release() on error	❌ No, Task 2 will wait forever (deadlock)
'''
print("Scenario 2")
#--------------------------------------------------------------------------------------------------------------------
import threading
import time

lock = threading.Lock()

def call_api(name):
    with lock:  # Lock auto-released even on error
        print(f"{name} acquired lock 🔒")
        if name == "Task-1":
            print(f"{name} calling API and got error ❌")
            raise Exception ("API failed!")  # simulate error
        print(f"{name} API success ✅")
        time.sleep(1)
    print(f"{name} released lock 🔓")

t1 = threading.Thread(target=call_api, args=("Task-1",))
t2 = threading.Thread(target=call_api, args=("Task-2",))
t3 = threading.Thread(target=call_api, args=("Task-3",))


t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("✅ All threads finished (no deadlock)")
