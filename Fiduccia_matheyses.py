# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:21:06 2025

@author: noelm
"""

def gain(cell_array,weight_array,i,f):
  gain=0
  c=f[i]
  for j in range(len(cell_array[i])):
    if f[cell_array[i][j]]==c:
      gain-=weight_array[i][j]
    else:
      gain+=weight_array[i][j]
  return gain
def f_m(N,E,S,W,f,s) :
  #initializing cell array
  cell_array=[[] for i in range(N)]
  weight_array=[[] for i in range(N)]
  for i in E:
    cell_array[i[0]].append(i[1])
    cell_array[i[1]].append(i[0])
    weight_array[i[0]].append(W[i])
    weight_array[i[1]].append(W[i])

  total_size=sum(S)
  free=[1 for i in range(N)]
  cut_size=0
  area=[S[i]*f[i] for i in range(N)]
  total_sum=sum(area)
  for i in E:
    if f[i[0]]!=f[i[1]]:
      cut_size+=W[i]
  min_cut_size=cut_size
  #finding pmax
  pmax=0
  for i in range(N):
    if sum(weight_array[i])>pmax:
      pmax=sum(weight_array[i])

  #computing gains and initializing bucket list
  g_l=[gain(cell_array,weight_array,i,f) for i in range(N)]
  b_l=[{} for i in range(-pmax,pmax+1)]
  for i in range(N):
    b_l[g_l[i]+pmax][i]=i
  global o
  o=[]
  x=0

  while x<N:

     first_key=-1
     for i in range(2*pmax,-1,-1):
      if len(b_l[i])==0:
        continue
      else:
        it=iter(b_l[i])
        flag=0
        while True:
          first_key = next(it,None)
          if first_key==None:
            break
          if f[first_key]==1:
            if total_sum-S[first_key]>(0.5-(s/2))*total_size:
              total_sum-=S[first_key]
              flag=1
              break
          else:
            if total_sum+S[first_key]<(0.5+(s/2))*total_size:
              flag=1
              total_sum+=S[first_key]
              break
        if flag==0:
          continue

        del b_l[i][first_key]
        free[first_key]=0
        if f[first_key]==0:
          f[first_key]=1
        else:
          f[first_key]=0
        break

     if first_key is None:
            break

     for i in range(len(cell_array[first_key])):
      if free[cell_array[first_key][i]]==1:
        del b_l[g_l[cell_array[first_key][i]]+pmax][cell_array[first_key][i]]
      if f[cell_array[first_key][i]]^f[first_key]==1:
        g_l[cell_array[first_key][i]]+=2*weight_array[first_key][i]
      else:
        g_l[cell_array[first_key][i]]-=2*weight_array[first_key][i]
      if free[cell_array[first_key][i]]==1:
        b_l[g_l[cell_array[first_key][i]]+pmax][cell_array[first_key][i]]=i

     if g_l[first_key]>0:
      cut_size-= g_l[first_key]
      if min_cut_size>=cut_size:
        min_cut_size=cut_size
        o=f[:]

     else:
        cut_size-= g_l[first_key]

     if first_key==-1:
       break
     x+=1

  if o==[]:
    return f,min_cut_size
  return o,min_cut_size
def coarsen(N,E,S,W):
  flag=[1 for i in range(N)]
  degree=[0 for i in range(N)]
  adj_list=[[] for i in range(N)]
  for u,v in E:
    #u,v=E[i]
    degree[u]+=W[(u,v)]
    degree[v]+=W[(u,v)]
    adj_list[u].append(v)
    adj_list[v].append(u)
  max_degree=max(degree)
  degree_array=[[] for i in range(max_degree+1)]
  for i in range(N):
    degree_array[degree[i]].append(i)

  super_vertex=[]
  for i in range(max_degree-1,-1,-1):
    if degree_array[i]==[]:
      continue
    else:
      for j in range(len(degree_array[i])):
        if flag[degree_array[i][j]]==1:
          flag[degree_array[i][j]]=0
          super_vertex.append([degree_array[i][j],])
          c=0


          for k in adj_list[degree_array[i][j]]:
            if c==10:
              break
            if flag[k]==1:
              flag[k]=0
              super_vertex[-1].append(k)
              c+=1
      if sum(flag)==0:
        break
  map=[0 for i in range(N)]
  for i in range(len(super_vertex)):
    for j in super_vertex[i]:
      map[j]=i
  size=[]
  for i in range(len(super_vertex)):
    size.append(len(super_vertex[i]))
  weight={}
  for u,v in E:
    if map[u]!=map[v]:
      weight[(map[u], map[v])] = weight.get((map[u], map[v]), 0) + W[(u, v)]
  return super_vertex,map,size,weight

def hier_part(N,E,c,s):
  vertex_data=[[[i,] for i in range(N)],]
  edge_data=[E,]
  size_data=[[1 for i in range(N)],]
  N_data=[N,]
  weight_data=[{i:1 for i in E},]

  for i in range(c):
    out=coarsen(N_data[i],edge_data[i],size_data[i],weight_data[i])
    vertex_data.append(out[0])
    edge_data.append(out[3].keys())
    size_data.append(out[2])
    weight_data.append(out[3])
    N_data.append(len(out[0]))
  a_size=0
  b_size=0
  f=[0 for i in range(N_data[-1])]
  for i in range(N_data[-1]):
    if a_size<=b_size:
      f[i]=0
      a_size+=size_data[-1][i]
    else:
      f[i]=1
      b_size+=size_data[-1][i]
  for i in range(len(vertex_data)-1,-1,-1):
    out=f_m(N_data[i],edge_data[i],size_data[i],weight_data[i],f,s)
    f=out[0]
    if i==0:
      return f
    o=[0 for l in range(N_data[i-1])]
    for k in range(len(vertex_data[i])):
      for j in vertex_data[i][k]:
        o[j]=f[k]
    f=o[:]

def cut_count(N, E, sol):
  count = 0
  assert len(sol) == N, "invalid sol size!"
  for e in E:
    if sol[e[0]] != sol[e[1]]:
      count += 1
  return count

def rand_graph(N, p = 0.05):
  import networkx as nx
  
  g = nx.erdos_renyi_graph(N, p)
  return g.edges

def test_hier_part():
  for N, c in [(1000,1),(10000,2)]:
    start_time = time.time() 
    E = rand_graph(N)
    sol = hier_part(N, E, c, 0.1)
    cut = cut_count(N, E, sol)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'N : {N}, c: {c} , cut : {cut} , total_edges :{len(E)} ,',f"Elapsed time: {elapsed_time:.6f} seconds")
    
   

import time
 
test_hier_part()
  
