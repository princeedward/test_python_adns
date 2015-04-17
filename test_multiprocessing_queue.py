import multiprocessing
import time


def worker(x, q, finished_flag):
    if x < 50000:
        q.put(x+100)
    else:
        finished_flag.set()


class WorkerProcess(multiprocessing.Process):

    def __init__(self, q, start_flag):
        multiprocessing.Process.__init__(self)
        self.jobs = q
        self.start_flag = start_flag
        self._finished = multiprocessing.Event()

    def run(self):
        self.start_flag.wait()
        while True:
            if self._finished.is_set() and self.jobs.empty():
                break
            num = self.jobs.get()
            worker(num, self.jobs, self._finished)


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
