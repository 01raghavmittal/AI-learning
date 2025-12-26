'''
🧩 LEVEL 2 – Thread Count & Synchronization
🧠 Problem 2: Monitor Active Threads

Modify Problem 1 to:

Print number of active threads at three points:

Before starting
While running
After completion

'''


from concurrent.futures import ThreadPoolExecutor, as_completed
import threading 
import time

def task(name):
    print(f"Task {name} started")
    print(f"active number of thread once program is starting is {threading.active_count()} ")
    time.sleep(2)
    print(f"Task {name} finished")
    print(f"active number of thread once program is finished is {threading.active_count()} ")

tasks = [i for i in range(1, 6)]
results=[]
errors = []

with ThreadPoolExecutor(max_workers=3) as executor:
    print(f"Total no of threads is {threading.active_count()}")
    futures = {executor.submit(task, t): t for t in tasks}

    for future in as_completed(futures):
        task_name = futures[future]
        try:
            result = future.result()  # waits for that task
            results.append(result)
        except Exception as e:
            errors.append(str(e))

print("\n✅ Successful results:", results)
print("❌ Errors:", errors)