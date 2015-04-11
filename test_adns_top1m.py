from multiprocessing import Pool
import httplib
import adns
import time

c = adns.init()
A = adns.rr.A

def dns_(domain):
  conn = httplib.HTTPConnection(domain)
  try:
    conn.connect()
  except Exception:
    pass
  conn.close()

def adns_(doamin):
  d = c.synchronous(doamin, A)
  if len(d[3]) > 0:
    conn = httplib.HTTPConnection(d[3][0])
    try:
      conn.connect()
    except Exception:
      pass
    conn.close()

def main():
  f = open('top-1m.csv','r')
  urls = [line.split(',')[1].strip() for line in f.readlines()]
  f.close()
  
  p = Pool(4)

  start = time.time()
  p.map(dns_, urls)
  print time.time() - start, " seconds for system dns resolver"

  start = time.time()
  p.map(adns_, urls)
  print time.time() - start, " seconds for adns resolver"

if __name__ == '__main__':
  main()