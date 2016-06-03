from numpy import random
import functools
import operator
from threading import Thread

def foldl(f, init, l):
  for x in l:
    init = f(init, x)
  return init

def foldl1(f, l):
  return foldl(f, l[0], l[1:])

def foldr(f, init, l):
  for x in reversed(l):
    init = f(x, init)
  return init

def foldr1(f, l):
  return foldr(f, l[-1], l[:-1])

def scanl(f, init, l):
  r = [init]
  for x in l:
    r.append(f(r[-1], x))
  return r

def scanl1(f, l):
  return scanl(f, l[0], l[1:])

def scanr(f, init, l):
  r = [init]
  for x in reversed(l):
    r.append(f(x, r[-1]))
  r.reverse()
  return r

def scanr1(f, l):
  return scanr(f, l[-1], l[:-1])

def zipWith(f, *sequences):
  return [f(*args) for args in zip(*sequences)]

def compose(*fs):
  "compose(f1, f2, ..., fn)(x) = f1(f2( ... fn(x)))"
  def composed(x):
    for f in reversed(fs):
      x = f(x)
    return x
  return composed

def deepMap(f, obj):
  if isinstance(obj, dict):
    return {k : deepMap(f, v) for k, v in obj.items()}
  if isinstance(obj, list):
    return [deepMap(f, x) for x in obj]
  return f(obj)

def deepValues(obj):
  if isinstance(obj, dict):
    for v in obj.values():
      yield from deepValues(v)
  elif isinstance(obj, list):
    for v in obj:
      yield from deepValues(v)
  else:
    yield obj

def deepZip(*objs):
  if len(objs) == 0:
    return []
  
  first = objs[0]
  if isinstance(first, dict):
    return {k : deepZip(*[obj[k] for obj in objs]) for k in first}
  if isinstance(first, list):
    return zipWith(deepZip, *objs)
  return objs

def flip(p):
  return random.binomial(1, p)

def product(xs):
  return functools.reduce(operator.mul, xs, 1.0)

def async_map(f, xs):
  n = len(xs)
  ys = n * [None]
  
  def run(i):
    ys[i] = f(xs[i])

  threads = n * [None]
  for i in range(n):
    threads[i] = Thread(target=run, args=[i])
    threads[i].start()
  
  def wait():
    for p in threads:
      p.join()
    return ys
  
  return wait

def chunk(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

