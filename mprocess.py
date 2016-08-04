import multiprocessing
import time
from pb_fun import syn

plist=[]
for i in range(10):
    s=syn()
    plist.append(s)

def f(p):
    p.syn_contact()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=10)              # start num worker processes

    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [pool.apply_async(f, (p,)) for p in plist]

    # make a single worker sleep for 1 secs
    res = pool.apply_async(time.sleep, (1,))
    print res.get(timeout=3600)
