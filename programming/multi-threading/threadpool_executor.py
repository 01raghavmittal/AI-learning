from concurrent.futures import ThreadPoolExecutor
import time

def task(name):
    print(f"👷‍♂️ Task {name} started")
    time.sleep(2)
    print(f"✅ Task {name} finished")

# Create a pool of 3 threads
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(task, "A")
    executor.submit(task, "B")
    executor.submit(task, "C")
    executor.submit(task, "D")
