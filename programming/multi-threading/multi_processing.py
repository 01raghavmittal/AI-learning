import multiprocessing as mp

def process():
    print("this is a new process")
    print("the process name is", mp.current_process())

if __name__ == "__main__":  
    proc = mp.Process(target=process)
    proc.start()
    proc.join()  # ✅ proper method call
