import threading
import time
import random

bar_1 = threading.Barrier(3, timeout=6)
bar_2 = threading.Barrier(2, timeout=6)

def print_work_a(bar):
    for i in range(1,6):
        czas = random.randint(0, 3)
        print('Starting of thread :', threading.current_thread().name + " " + " --> " + str(czas) + "śpie -->" + str(i) )
        time.sleep(czas)
        if czas == 3:
            bar.reset()
        bar.wait()
        

def print_work_b():
    print('Starting of thread :', threading.current_thread().name)
    
    print('Finishing of thread :', threading.current_thread().name)

a = threading.Thread(target=print_work_a, args=(bar_1,), name='Thread-a', daemon=True)
b = threading.Thread(target=print_work_a, args=(bar_1,), name='Thread-b', daemon=True)
c = threading.Thread(target=print_work_a, args=(bar_1,), name='Thread-c', daemon=True)
a.start()
b.start()
c.start()
bar_2 = threading.Barrier(2, timeout=6)
a = threading.Thread(target=print_work_a, args=(bar_2,), name='Thread-uwaga-a', daemon=True)
b = threading.Thread(target=print_work_a, args=(bar_2,), name='Thread-uwaga-b', daemon=True)
a.start()
b.start()

time.sleep(10)