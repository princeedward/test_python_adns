import multiprocessing
import adns
import logging

c = adns.init()
rr = adns.rr.A

# class MyManager(multiprocessing.managers.SyncManager):
#     pass
#
# MyManager.register('Adns', c)

def worker(x, q, p):
    host = q.get()
    # print host
    c.submit(host, rr)
    p.put(1, False)


def main():
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    f = open("top-1m.csv", "r")
    urls = [line.split(',')[1].strip() for line in f.readlines()]
    f.close()
    urls = urls[:500]

    resolved_list = []

    m = multiprocessing.Manager()
    q = m.Queue()
    for each in urls:
        q.put(each)
    process_monitor = m.Queue()
    for each in xrange(20):
        process_monitor.put(1)
    p = multiprocessing.Pool(processes=20)
    while not q.empty():
        process_monitor.get()
        p.apply_async(worker, args=(1, q, process_monitor))
        for query in c.completed():
            answer = query.check()
            resolved_list.append(answer)
            print answer
    #while not len(resolved_list) == 500:
    #    for query in c.completed():
    #        answer = query.check()
    #        resolved_list.append(answer)
    #        print answer

if __name__ == "__main__":
    main()
