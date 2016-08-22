from random import randint

def strategy1(n):
  bins = [0] * n
  for i in range(n):
    j = randint(0, n - 1) # both inclusive
    bins[j] += 1
  #print bins
  return max(bins)

def strategy2(n):
  bins = [0] * n
  for i in range(n):
    j = randint(0, n - 1) # both inclusive
    k = randint(0, n - 1) # both inclusive
    if bins[j] < bins[k]:
      bins[j] += 1
    elif bins[k] < bins[j]:
      bins[k] += 1
    else:
      l = randint(0, 1)
      if l == 0:
        bins[j] += 1
      else:
        bins[k] += 1
  #print bins
  return max(bins)

def strategy3(n):
  bins = [0] * n
  for i in range(n):
    j = randint(0, n - 1) # both inclusive
    k = randint(0, n - 1) # both inclusive
    l = randint(0, n - 1) # both inclusive
    if bins[j] < bins[k] and bins[j] < bins[l]:
      bins[j] += 1
    elif bins[k] < bins[j] and bins[k] < bins[l]:
      bins[k] += 1
    elif bins[l] < bins[j] and bins[l] < bins[k]:
      bins[l] += 1
    elif bins[j] == bins[k] and bins[j] < bins[l]:
      r = randint(0, 1)
      if r == 0:
        bins[j] += 1
      else:
        bins[k] += 1
    elif bins[j] == bins[l] and bins[j] < bins[k]:
      r = randint(0, 1)
      if r == 0:
        bins[j] += 1
      else:
        bins[l] += 1
    elif bins[k] == bins[l] and bins[k] < bins[j]:
      r = randint(0, 1)
      if r == 0:
        bins[k] += 1
      else:
        bins[l] += 1
    else:
      r = randint(0, 2)
      if r == 0:
        bins[j] += 1
      elif r == 1:
        bins[k] += 1
      else:
        bins[l] += 1   
  #print bins
  return max(bins)

def strategy4(n):
  bins = [0] * n
  for i in range(n):
    j = randint(0, n/2 - 1) # both inclusive
    k = randint(n/2, n - 1) # both inclusive
    if bins[j] <= bins[k]:
      bins[j] += 1
    else:
      bins[k] += 1
  #print bins
  return max(bins)

def main():
  n = [20, 200, 2000, 20000, 200000, 2000000, 20000000]
  for k in n:
    strategies = [[], [], [], []]
    for i in range(40):
      x = strategy1(k)
      strategies[0].append(x)
      x = strategy2(k)
      strategies[1].append(x)
      x = strategy3(k)
      strategies[2].append(x)
      x = strategy4(k)
      strategies[3].append(x)
    print 'n:', k
    print 'Strategy 1:', strategies[0]
    print 'Strategy 2:', strategies[1]
    print 'Strategy 3:', strategies[2]
    print 'Strategy 4:', strategies[3]

if __name__ == '__main__':
  main()     
