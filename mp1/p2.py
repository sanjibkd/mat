import hashlib as hl
import sys
#import Set
from random import shuffle

class CountMinSketch:

  def __init__(self, b, l, k, c):
    self.b = b
    self.l = l
    self.cms = [[0 for bb in range(b)] for ll in range(l)] 
    self.n = 0
    self.k = k
    self.hh = set()
    self.c = c

  def reset(self):
    for i in range(self.l):
      for j in range(self.b):
        self.cms[i][j] = 0
    self.n = 0
    self.hh.clear()
        
  def update_cms(self, trial, key, value):
    if self.c:
      self.__update_cms_cons(trial, key, value)
    else:
      self.__update_cms(trial, key, value)
    self.n += value
    f = self.cms_estimate(trial, key)
    if self.k * f < self.n:
      self.hh.discard(key)
    else:
      self.hh.add(key)

  def __update_cms(self, trial, key, value):
    h = md5hash(key, trial)
    for j in range(self.l): # which table
      h1 = h[2 * j : 2 * j + 2]
      self.cms[j][int(h1, 16)] += value
      
  def __update_cms_cons(self, trial, key, value):
    h = md5hash(key, trial)
    minf = sys.maxint
    for j in range(self.l): # which table
      h1 = h[2 * j : 2 * j + 2]
      val = self.cms[j][int(h1, 16)]
      if val < minf:
        minf = val
    for j in range(self.l): # which table
      h1 = h[2 * j : 2 * j + 2]
      val = self.cms[j][int(h1, 16)]
      if val == minf:
        self.cms[j][int(h1, 16)] += value
      
  def cms_estimate(self, trial, key):
    h = md5hash(key, trial)
    min1 = sys.maxint
    for j in range(self.l): # which table
      h1 = h[2 * j : 2 * j + 2]
      min1 = min(min1, self.cms[j][int(h1, 16)])
    return min1

  def estimate_heavy_hitters(self, trial):
    non_hh = set()
    for key in self.hh:
      f = self.cms_estimate(trial, key)
      if self.k * f < self.n:
        non_hh.add(key)
    self.hh.difference_update(non_hh)
    return self.hh

def forward_trial(cms_obj, trial):
  for i in range(1, 10):
    for x in range(1000 * (i - 1) + 1, 1000 * i + 1): # data elements
      for v in range(i):
        cms_obj.update_cms(trial, x, 1)
  for i in range(1, 51):
    x = 9000 + i
    for v in range(i * i):
      cms_obj.update_cms(trial, x, 1)
#  print cms_obj.cms

def forward_count_min_sketch(cms_obj):
  trials = 10
  sum1 = 0
  for trial in range(trials): # 10 trials
    print 'Trial', trial
    forward_trial(cms_obj, trial)
    sum1 += cms_obj.cms_estimate(trial, 9050)
    hh = cms_obj.estimate_heavy_hitters(trial)
    print len(hh), hh
    cms_obj.reset()
  avg = sum1/trials
  print 'Avg. estimate of freq. of 9050 for forward order', avg

def backward_trial(cms_obj, trial):
  for i in range(50, 0, -1):
    x = 9000 + i
    for v in range(i * i):
      cms_obj.update_cms(trial, x, 1)
  for i in range(9, 0, -1):
    for x in range(1000 * i, 1000 * (i - 1), -1): # data elements
      for v in range(i):
        cms_obj.update_cms(trial, x, 1)
#  print cms_obj.cms

def backward_count_min_sketch(cms_obj):
  trials = 10
  sum1 = 0
  for trial in range(trials): # 10 trials
    print 'Trial', trial
    backward_trial(cms_obj, trial)
    sum1 += cms_obj.cms_estimate(trial, 9050)
    hh = cms_obj.estimate_heavy_hitters(trial)
    print len(hh), hh
    cms_obj.reset()
  avg = sum1/trials
  print 'Avg. estimate of freq. of 9050 for backward order', avg

def random_trial(cms_obj, trial):
  data = []
  for i in range(50, 0, -1):
    x = 9000 + i
    for j in range(i * i):
      data.append(x)
  for i in range(9, 0, -1):
    for x in range(1000 * i, 1000 * (i - 1), -1): # data elements
      for j in range(i):
        data.append(x)
  shuffle(data)
  for i in data:
    cms_obj.update_cms(trial, i, 1)
#  print cms_obj.cms

def random_count_min_sketch(cms_obj):
  trials = 10
  sum1 = 0
  for trial in range(trials): # 10 trials
    print 'Trial', trial
    random_trial(cms_obj, trial)
    sum1 += cms_obj.cms_estimate(trial, 9050)
    hh = cms_obj.estimate_heavy_hitters(trial)
    print len(hh), hh
    cms_obj.reset()
  avg = sum1/trials
  print 'Avg. estimate of freq. of 9050 for random order', avg

def count_heavy_hitters():
  freqs = [0] * 9051
  for i in range(1, 10):
    for x in range(1000 * (i - 1) + 1, 1000 * i + 1): # data elements
      freqs[x] = i
  for i in range(1, 51):
    x = 9000 + i
    freqs[x] = i * i
  sum1 = sum(freqs)
  print 'Sum of freqs:', sum1
  for i in range(1, 9051):
    if freqs[i] * 100 >= sum1:
      print i, freqs[i]

def md5hash(x, i):
  y = str(x * 10 + i)
  return hl.md5(y.encode('utf-8')).hexdigest()

def main():
  b = 256
  l = 4
  k = 100
  cms_obj = CountMinSketch(b, l, k, True) 
  #cms_obj.count_min_sketch()
#count_heavy_hitters()
  forward_count_min_sketch(cms_obj)
  backward_count_min_sketch(cms_obj)
  random_count_min_sketch(cms_obj)

if __name__ == '__main__':
  main()
