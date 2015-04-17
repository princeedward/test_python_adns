import threading
import adns
import logging
import Queue

# rr = adns.rr.A


def worker(q, c, f, n):
    print q.qsize()
    with n:
        if q.empty():
            print "Nothing in the queue"
            f.set()
        else:
            host = q.get()
            # print host
            c.submit(host, adns.rr.A)
        n.notify()


class WorkerProcess(threading.Thread):

    def __init__(self, params):
        threading.Thread.__init__(self)
        self._start_flag = params["start"]
        self._jobs = params["jobs"]
        print self.name, ":queue length:", self._jobs.qsize()
        self._adns = params["adns"]
        self._new_job = params["notify"]
        self._finished = threading.Event()

    def run(self):
        self._start_flag.wait()
        while not self._finished.is_set():
            worker(self._jobs, self._adns, self._finished, self._new_job)


def main():
    # logger = threading.log_to_stderr()
    # logger.setLevel(logging.INFO)
    f = open("/home/edward/Projects/test_python_adns/top-1m.csv", "r")
    urls = [line.split(',')[1].strip() for line in f.readlines()]
    f.close()
    num = 500
    # Put urls into queue
    urls = urls[:num]
    q = Queue.Queue()
    count = 0
    for each in urls:
        q.put(each)
        count += 1
    print count
    print q.qsize()
    # other initialization
    resolved_list = []
    start_flag = threading.Event()
    adns_state = adns.init()
    new_job = threading.Condition()
    # build process pools
    opts = {"start": start_flag, "jobs": q, "adns": adns_state, "notify": new_job}
    pool = [WorkerProcess(opts) for i in xrange(1)]
    for each in pool:
        each.start()

    start_flag.set()


    while True:
        with new_job:
            # TODO: Figure out why adns library crashed even with a lock
            # It is not successfully passed into threads
            for query in adns_state.completed():
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
