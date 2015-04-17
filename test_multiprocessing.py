import multiprocessing
import time
# import sys
# import logging


def worker(x, q, p):
    # print x
    if x < 5000:
        q.put(x+100)
    p.put(1)


def main():
    # logger = multiprocessing.log_to_stderr()
    # logger.setLevel(logging.INFO)
    m = multiprocessing.Manager()
    print "Building working queue"
    start = time.time()
    # q = m.Queue()
    q = m.Queue()
    for i in xrange(100):
        q.put(i)
    print time.time() - start, " seconds"
    print "Creating pools:"
    start = time.time()
    p = multiprocessing.Pool(processes=4)
    print time.time() - start, " seconds"
    print "Preparing process monitor queue"
    start = time.time()
    # process_monitor = m.Queue()
    process_monitor = m.Queue()
    for i in xrange(4):
        process_monitor.put(1)
    print time.time() - start, " seconds"

    start = time.time()
    while not q.empty():
        if process_monitor.empty():
            continue
        process_monitor.get()
        num = q.get()
        # print num
        p.apply_async(worker, args=(num, q, process_monitor,))
    print "Finished all the jobs at", time.time() - start, "seconds"

if __name__ == "__main__":
    main()
