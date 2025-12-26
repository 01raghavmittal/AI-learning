'''
🧩 LEVEL 1 – Basic Multithreading Understanding
🧠 Problem 1: Simulate Multiple Tasks

Write a program that:

Creates 5 threads using ThreadPoolExecutor.
Each thread runs a function that:
Prints “Task X started”
Sleeps for a random time between 1–3 seconds
Prints “Task X finished”

You should observe:
Tasks start almost together.
Tasks finish in random order (depending on sleep time).
💡 Tests your understanding of concurrent execution.
'''

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(name):
    print(f"Task {name} started")
    time.sleep(2)
    print(f"Task {name} finished")

tasks = [i for i in range(1, 6)]
results=[]
errors = []

with ThreadPoolExecutor(max_workers=3) as executor:
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
