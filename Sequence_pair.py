# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 09:24:18 2025

@author: noelm
"""

import math
import random
class Module:
    def __init__(self, name, area, aspect_ratios):
        self._name = name
        self._area = area
        self._wh = [(math.sqrt(area*r), math.sqrt(area/r)) for r in aspect_ratios]
    def __repr__(self):
        return f"{self._name} area:{self._area} xy:{self._wh}"
class SeqPair:
    def __init__(self, modules):
        self._pos = [i for i in range(len(modules))] # positive sequence
        self._neg = [i for i in range(len(modules))] # negative sequence
        self._ap = [0 for i in range(len(modules))] # aspect ratio choice
        self._coord = [(0,0) for i in range(len(modules))]
        self._w = 0
        self._h = 0


    def perturb(self, modules):

      p_type = random.choice(["swap_pos", "swap_neg", "change_aspect"])

      if p_type == "swap_pos":
          i, j = random.sample(range(len(modules)), 2)
          self._pos[i], self._pos[j] = self._pos[j], self._pos[i]

      elif p_type == "swap_neg":
          i, j = random.sample(range(len(modules)), 2)
          self._neg[i], self._neg[j] = self._neg[j], self._neg[i]

      elif p_type == "change_aspect":
          i = random.randint(0, len(modules) - 1)
          self._ap[i] = (self._ap[i] + 1) % len(modules[i]._wh)

      return self

    def costEval(self, modules):

      pos_index={self._pos[i]:i for i in range(len(modules))}
      neg_index={self._neg[i]:i for i in range(len(modules))}
      n = len(modules)
      hcg=[[0 for i in range(n)] for j in range(n)]
      max_x=0
      max_y=0

      h_in={i:0 for i in range(n)}
      vcg=[[0 for i in range(n)] for j in range(n)]
      v_in={i:0 for i in range(n)}
      x_coords=[0 for i in range(n)]
      y_coords=[0 for i in range(n)]
      for i in range(n):
        for j in range(i+1,n):
          mod_i, mod_j = self._pos[i], self._pos[j]
          if pos_index[mod_i]<pos_index[mod_j] and neg_index[mod_i]<neg_index[mod_j]:
            hcg[mod_j][mod_i]=1
            h_in[mod_j]+=1

          else:
            vcg[mod_j][mod_i]=1
            v_in[mod_j]+=1

      h_fixed=[0 for i in range(n)]
      v_fixed=[0 for i in range(n)]
      for i in range(n):
          if h_in[i]<=0:
            h_fixed[i]=1
          if v_in[i]<=0:
            v_fixed[i]=1
      while True :

        for i in range(n):
          if h_fixed[i]==1:
            continue
          c=0
          for j in range(n):

            if hcg[i][j]==1:
              if h_fixed[j]==1:
                c+=1

                x_coords[i]=max(x_coords[i],x_coords[j]+modules[j]._wh[self._ap[j]][0])
          if c==h_in[i]:
            h_fixed[i]=1

        if sum(h_fixed)==n:
          break


      while True:
        for i in range(n):
          if v_fixed[i]==1:
            continue
          c=0
          for j in range(n):

            if vcg[i][j]==1:
              if v_fixed[j]==1:
                c+=1

                y_coords[i]=max(y_coords[i],y_coords[j]+modules[j]._wh[self._ap[j]][1])
          if c==v_in[i]:
            v_fixed[i]=1
        if sum(v_fixed)==n:
          break


      module_sizes = [modules[i]._wh[self._ap[i]] for i in range(n)]
      max_x = max(x_coords[i] + module_sizes[i][0] for i in range(n))
      max_y = max(y_coords[i] + module_sizes[i][1] for i in range(n))

      self._coord = [(x_coords[i], y_coords[i]) for i in range(n)]
      self._w = max_x
      self._h = max_y

      a=(max_x,max_y)

      return a

import copy

def accept(delC, T,b):
    if delC <= 0:
        return True
    
    
    return random.random() < math.exp(-delC / T)

# S = Initial sequence pair, choice of aspect ratio
# ARmin, ARmax: minimum/maximum allowed aspect ratio of solution
def simulated_annealing(Tmin, Tmax, N, alpha, S, modules, ARmin, ARmax, plot):
    assert(alpha < 1. and Tmin < Tmax)
    T = Tmax
    a=S.costEval(modules)
    C = a[0]*a[1]
    q=0
    if (a[0]/a[1]<ARmin) or (a[0]/a[1]>ARmax):
              q=1
    minC = C
    minS = copy.deepcopy(S)
    Clist = []
    Temp = []

    while T > Tmin:
        for i in range(N):
            Snew = S.perturb(modules)
            x_,y_=Snew.costEval(modules)
            Cnew = x_*y_
            b=0
            if (x_/y_<ARmin) or (x_/y_>ARmax):
              b=1
            if accept(Cnew - C, T,b):
                C, S = Cnew, Snew
            if q==1:
              if  (ARmin < x_/y_) and (ARmax >x_/y_) :
                minC, minS = Cnew, copy.deepcopy(Snew)
                q=0



            if (minC >= Cnew)and (ARmin < x_/y_) and (ARmax >x_/y_) :
                minC, minS = Cnew, copy.deepcopy(Snew)
            Clist.append(Cnew)
            Temp.append(T)
        T = T * alpha
        #print(minC)

    if plot:
        import matplotlib.pyplot as plt
        plt.plot(Temp, Clist)
        plt.xlim(max(Temp), min(Temp))
        plt.xscale('log')

    return minS, minC
def sp_floorplan(modules, ARmin, ARmax):
  S = SeqPair(modules)
  Tmax = sum([i._area for i in modules])
  Smin, Cmin = simulated_annealing(1, Tmax, 100, 0.9, S, modules, ARmin, ARmax, False)
  assert(len(Smin._coord) == len(Smin._ap) and (len(Smin._coord) == len(modules)))
  sol = [(Smin._coord[i], m[i]._wh[Smin._ap[i]], m[i]._name) for i in range(len(modules)) ]
  return (sol, Cmin)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot(coords):
    """Plots the floorplan with rectangles representing modules."""
    fig, ax = plt.subplots()
    ax.plot([0, 0])
    ax.set_aspect('equal')  # Fixed incorrect string quote

    ax.set_xlim(0, max([r[0][0] + r[1][0] for r in coords]))
    ax.set_ylim(0, max([r[0][1] + r[1][1] for r in coords]))

    for i, r in enumerate(coords):
        x=i%4
        
        if x==3: hatch, color = '/+', 'red'
        elif x==2: hatch, color = '///', 'green'
        elif x==1: hatch, color = '/\\/', 'blue'
        else : hatch, color = '\\', 'gray'  # Default case

        ax.add_patch(Rectangle(
            r[0], r[1][0], r[1][1],
            edgecolor=color, facecolor=color,
            hatch=hatch, fill=False, lw=2
        ))

        ax.text(r[0][0] + r[1][0] // 2, r[0][1] + r[1][1] // 2, r[2], fontsize=8)

    plt.show()  # Ensure it is properly indented
m = [Module('a', 16, [0.25, 4]), Module('b', 32, [2.0, 0.5]), Module('c', 27, [1./3, 3.]),
Module('d', 6, [6])]
sol, area = sp_floorplan(m, 0.75, 1.33)
plot(sol)
print(area)
print(sol)

m = [Module(str(i), random.randint(10,100), [1.]) for i in range(10)]
sol, area = sp_floorplan(m, 0.5, 2)
plot(sol)
print(area)
print(sol)
