import hashlib as hl

def md5hash(x, i):
  y = str(x * 10 + i)
  return hl.md5(y.encode('utf-8')).hexdigest()

def count_min_sketch():
  b = 256
  l = 4
  trials = 10
  for trial in range(trials): # 10 trials
    cms = [[0 for bb in range(b)] for ll in range(l)]
    sum1 = 0
    for i in range(1, 10):
      for x in range(1000 * (i - 1) + 1, 1000 * i + 1): # data elements
          h = md5hash(x, trial)
          for j in range(l): # which table
              h1 = h[2*j:2*j+2]
              tmp = int(h1, 16)
              cms[j][tmp] = cms[j][tmp] + i

          sum1 += i

    for i in range(1, 51):
      x = 9000 + i
      h = md5hash(x, trial)
      for j in range(l): # which table
        h1 = h[2*j:2*j+2]
        cms[j][int(h1, 16)] += i*i
      sum1 += i*i
    print 'Trial', trial
    print cms

def main():
  count_min_sketch()

if __name__ == '__main__':
  main()
