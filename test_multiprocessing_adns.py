import multiprocessing
import adns
import logging

rr = adns.rr.A


def worker(q, c, f, n):
    print q.qsize()
    with n:
        if q.empty():
            print "Nothing in the queue"
            f.set()
        else:
            host = q.get()
            # print host
            c.submit(host, rr)
        n.notify()


class WorkerProcess(multiprocessing.Process):

    def __init__(self, params):
        multiprocessing.Process.__init__(self)
        self._start_flag = params["start"]
        self._jobs = params["jobs"]
        print self.name, ":queue length:", self._jobs.qsize()
        self._adns = params["adns"]
        self._new_job = params["notify"]
        self._finished = multiprocessing.Event()

    def run(self):
        self._start_flag.wait()
        while not self._finished.is_set():
            worker(self._jobs, self._adns, self._finished, self._new_job)


def main():
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    f = open("/home/edward/Projects/test_python_adns/top-1m.csv", "r")
    urls = [line.split(',')[1].strip() for line in f.readlines()]
    f.close()
    num = 500
    # Put urls into queue
    urls = urls[:num]
    q = multiprocessing.Queue()
    count = 0
    for each in urls:
        q.put(each)
        count += 1
    print count
    print q.qsize()
    # other initialization
    resolved_list = []
    start_flag = multiprocessing.Event()
    c = adns.init()
    new_job = multiprocessing.Condition()
    # build process pools
    opts = {"start": start_flag, "jobs": q, "adns": c, "notify": new_job}
    pool = [WorkerProcess(opts) for i in xrange(1)]
    for each in pool:
        each.start()

    start_flag.set()

    while True:
        with new_job:
            for query in c.completed():
                answer = query.check()
                resolved_list.append(answer)
                print answer
            new_job.wait()
        if len(resolved_list) == count:
            break

    for each in pool:
        each.join()

if __name__ == "__main__":
    main()
