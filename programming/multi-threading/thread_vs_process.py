import threading, multiprocessing, time

def cpu_task():
    print(sum(i * i for i in range(10_000_000)))

# Run with Threads
threads = [threading.Thread(target=cpu_task) for _ in range(4)]
start = time.time()
for t in threads: t.start()
for t in threads: t.join()
print("Threading time:", time.time() - start)

# Run with Processes
processes = [multiprocessing.Process(target=cpu_task) for _ in range(4)]
start = time.time()
for p in processes: p.start()
for p in processes: p.join()
print("Multiprocessing time:", time.time() - start)

