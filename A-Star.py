# -*- coding: utf-8 -*-



import math
import heapq as hq

class Vertex:
  def __init__(self, x, y, cost=math.inf, parent=None, nbrs=None):
    self._xy = (x, y)

    self._g=0
    self._h=0
    self._cost = self._g+self._h
    self._parent = parent
    self._nbrs = nbrs
  def __lt__(self, r):
    return self._cost < r._cost
  def __eq__(self, r):
    return self._xy == r._xy
  def __repr__(self):
    return f'(xy:{self._xy}, cost:{self._cost})'

class priority_queue:
  def __init__(self, vertices = []):
    self._vertices = vertices[:]
    self._q = vertices[:]
    hq.heapify(self._q)
  def push(self, v):
    hq.heappush(self._q, v)
  def pop(self):
    return(hq.heappop(self._q))
  def update(self, v, cost):
    try: i = self._q.index(v)
    except ValueError: i = None
    if i is not None:
      self._q[i]._cost = cost
      hq.heapify(self._q)
  def updateIndex(self, i, cost):
    assert i < len(self._q)
    self._vertices[i]._cost = cost
    hq.heapify(self._q)
  def empty(self):
    return len(self._q) == 0
  def __contains__(self, v):
    return v in self._q
  def __repr__(self):
    return str(self._q)

def dist(u, v):
  return abs(u._xy[0] - v._xy[0]) + abs(u._xy[1] - v._xy[1])

def dijkstra(V, s, t):
  for v in V:
    v._cost, v._parent = math.inf, None
  s._cost = 0
  Q = priority_queue(V)
  while not Q.empty():
    u = Q.pop()
    if u == t: break
    for v in u._nbrs:
      if v in Q:
        newcost = u._cost + dist(u, v)
        if newcost < v._cost:
          Q.update(v, newcost)
          v._parent = u
  path = [t]
  while path[-1]._parent is not None:
    path.append(path[-1]._parent)
  return path



def astar(V, s, t):
  for v in V:
    v._g,v._h, v._parent,v._cost = math.inf,dist(v,t), None,math.inf
  s._g = 0
  s._cost= s._g + s._h
  Q = priority_queue(V)
  while not Q.empty():
    u = Q.pop()
    if u == t: break
    for v in u._nbrs:
      if v._g > u._g + dist(u, v):
        v._g = u._g + dist(u, v)
        v._parent = u
        if v in Q:
          Q.update(v, v._g + v._h)
        else:

          Q.push(v)



  path = [t]
  while path[-1]._parent is not None:
    path.append(path[-1]._parent)
  return path

Vertices = [Vertex(0, 0, -1), Vertex(0,10,-1), Vertex(5,5,-1), Vertex(5,10,-1), Vertex(10,10,-1)]
Vertices[0]._nbrs = [Vertices[1], Vertices[2]]
Vertices[1]._nbrs = [Vertices[0], Vertices[4]]
Vertices[2]._nbrs = [Vertices[1], Vertices[3]]
Vertices[3]._nbrs = [Vertices[2], Vertices[4]]
Vertices[4]._nbrs = [Vertices[1], Vertices[3]]
for alg in [dijkstra, astar]:
  src = Vertices[0]
  tgt = Vertices[-1]
  print('src :', src, ' tgt :', tgt, 'path :', alg(Vertices, src, tgt))

import random
Vertices = [Vertex(random.randint(0,1000), random.randint(0,1000), -1) for i in range(10000)]

for v in Vertices:
  if v._nbrs is None: v._nbrs = list()
  for i in range(random.randint(1, 2)):
    nbr = Vertices[random.randint(0, len(Vertices)-1)]
    if nbr._nbrs is None: nbr._nbrs = list()
    v._nbrs.append(nbr)
    nbr._nbrs.append(v)
for alg in [dijkstra, astar]:
  src = Vertices[0]
  tgt = Vertices[-1]
  import time
  t = time.time()
  path = alg(Vertices, src, tgt)
  print('src :', src, ' tgt :', tgt, 'path :', path, time.time() - t)