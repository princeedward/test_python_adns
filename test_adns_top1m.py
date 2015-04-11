from multiprocessing import Pool
import adns
import time
import socket

c = adns.init()
A = adns.rr.A


def dns_(domain):
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        pass

def adns_(doamin):
    c.synchronous(doamin, A)


def main():
    f = open('top-1m.csv', 'r')
    urls = [line.split(',')[1].strip() for line in f.readlines()]
    f.close()
    urls = urls[:1000]

    p = Pool(100)

    start = time.time()
    p.map(dns_, urls)
    print time.time() - start, " seconds for system dns resolver"

    start = time.time()
    p.map(adns_, urls)
    print time.time() - start, " seconds for adns resolver"

if __name__ == '__main__':
    main()
