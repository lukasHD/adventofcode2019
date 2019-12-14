import threading
import queue
import time

def do_work(item):
    time.sleep(5)

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(item)
        do_work(item)
        q.task_done()

q = queue.Queue()
num_worker_threads = 5
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(20):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()