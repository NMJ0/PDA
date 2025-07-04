# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 09:17:44 2025

@author: noelm
"""


#!/usr/bin/env python3

import random

def unitClauses(f):
  return [c[0] for c in f if 1 == len(c)]
        
def pureLiterals(f, m):
  plc = [i for i in range(1, len(m)) if None == m[i]]
  p = []
  values=[]
  for i in plc:
      flag=0
      flag_1=0
      for j in f:
          if (i in j):
              if flag==-1:
                  flag_1=1
                  break
              flag=1
              
          if -i in j:
              if flag==1:
                  flag_1=1
                  break
              flag=-1
      if flag_1==0:
          p.append(i)
          values.append(flag)
  return p,values


def pickBranchingLiteral(m):
  l = [i for i in range(1, len(m)) if 0 == m[i]]
  return l[0] if len(l) else None
#return random.choice(l)

def dpll(f, m):
  
  if len(f)==0:
        
        return True,m 
  for c in f:
      if len(c)==0:
         print(f)
         return False,m
       
  p,values=pureLiterals(f, m)
  
  for i in range(len(p)):
      m[p[i]]=values[i]
      for j in range(len(f)-1,-1,-1):
          if p[i] in f[j]:
              f.pop(j)
  if len(f)==0:
        
        return True,m 
  for c in f:
      if len(c)==0:
         
         return False,m
  u_c=unitClauses(f)
  
  for i in u_c:
      if -i in u_c:
          
          return False,m
  u_c_1=[]
  for i in u_c:
      if i not in u_c_1:
          u_c_1.append(i)
            
  for c in u_c_1:
      
      v=c
      
      if v>0:
           m[abs(v)]=1
      else :
          m[abs(v)]=-1
      for j in range(len(f)-1,-1,-1):
          if v in f[j]:
              f.pop(j)
              continue
          if -v in f[j]:
              f[j].remove(-v)
  if len(f)==0:
      
        return True,m 
  for c in f:
      if len(c)==0:
         
         return False,m
    
  b=pickBranchingLiteral(m)
 
  new_f1 = []
  for i in f:
      new_f1.append(i[:])
  new_f2 = []
  for i in f:
      new_f2.append(i[:])
  assert new_f1==new_f2

  new_f1.append([b,])
  m1=m[:]
  
  result1, m1 = dpll(new_f1, m1) 
  if result1:
     return result1, m1
   
  new_f2.append([-b,])
  m2=m[:]
  return dpll(new_f2, m2)
    
def loadCNFFile(fn):
  numvars = 0
  numclauses = 0
  clauses = []
  with open(fn, 'r') as fs:
    for line in fs:
      if line[0] == '%': break
      # p is the description line
      if line[0] == 'p':
        numvars = int(line.split()[2])
        numclauses = int(line.split()[3])
        continue
      # c is a comment
      if line[0] == 'c': continue
      if numvars > 0:
        tmp = line.split()
        tmp = [int(tmp[i]) for i in range(len(tmp) - 1)]
        clauses.append(tmp)
        assert abs(tmp[0]) <= numvars and abs(tmp[1]) <= numvars and abs(tmp[2]) <= numvars
  assert len(clauses) == numclauses
  return numvars, clauses

numvars, clauses = loadCNFFile('uf50-0500.cnf')

m = [0 for i in range(numvars + 1)]

ret, m = (dpll(clauses, m))
print(ret)
for i in range(len(m)):
    if m[i]==None:
        continue
    if m[i]>0:
        m[i]=True
print([(i if m[i] == True else -i) for i in range(1, len(m))])

'''
if __name__ == '__main__':
  import argparse

  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--cnf", type=str, default="", help='<cnf file>')
  args = ap.parse_args()
  if args.cnf != "":
    print(f"CNF file  : {args.cnf}")
    numvars, clauses = loadCNFFile(args.cnf)
    m = [None for i in range(numvars + 1)]
    ret, m = (dpll(clauses, m))
    print([(i if m[i] == True else -i) for i in range(1, len(m))])
'''