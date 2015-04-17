import multiprocessing
import time


def worker(x, q):
    print x
    if x < 5000:
        q.put(x+100)


class WorkerProcess(multiprocessing.Process):

    def __init__(self, q, start_flag):
        multiprocessing.Process.__init__(self)
        self.jobs = q
        self.start_flag = start_flag

    def run(self):
        self.start_flag.wait()
        while not self.jobs.empty():
            num = self.jobs.get()
            worker(num, self.jobs)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    for i in xrange(100):
        q.put(i)
    start_flag = multiprocessing.Event()

    process_pool = [WorkerProcess(q, start_flag) for i in xrange(4)]
    start = time.time()
    for idx, each in enumerate(process_pool):
        each.start()

    start_flag.set()

    for each in process_pool:
        each.join()

    print "Finished all the jobs at", time.time() - start, "seconds"
