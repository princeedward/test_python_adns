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

def adns_(doamin):
  d = c.synchronous(doamin, A)
  if len(d[3]) > 0:
    conn = httplib.HTTPConnection(d[3][0])
    try:
      conn.connect()
    except Exception:
      pass

def main():
  f = open('test_domains.txt','r')
  doc = f.read()
  f.close()
  urls = doc.split('\n')

  p = Pool(len(urls))

  start = time.time()
  p.map(dns_, urls)
  print time.time() - start, " seconds for system dns resolver"

  start = time.time()
  p.map(adns_, urls)
  print time.time() - start, " seconds for adns resolver"

if __name__ == '__main__':
  main()