import math
import numpy as np
from copy import copy #highly important stuff to copy objects without adress!!!
def dot_prod(u,v):
    return u[0]*v[0]+u[1]*v[1] 

def norm(v):
    return math.sqrt(dot_prod(v,v))
def d(u,v):
    return norm([u[0]-v[0],u[1]-v[1]])
def isLeft(P0,P1,P2):
    return (P1.LONG-P0.LONG)*(P2.LAT*P0.LAT)-(P2.LONG-P0.LONG)*(P1.LAT-P0.LAT)
def p2seg(S,P):
    
    v=[S[1].LONG-S[0].LONG,S[1].LAT-S[0].LAT]
    u=[P.LONG-S[0].LONG,P.LAT-S[0].LAT]
    di=0
    c1=dot_prod(u,v)
    if c1<=0:
        di=d([P.LONG, P.LAT],[S[0].LONG,S[0].LAT])
        return di
            

    c2=dot_prod(v,v)
    if c2<=c1:
        di=d([P.LONG, P.LAT],[S[1].LONG,S[1].LAT])
        return di
            
    b=c1/c2
    k=copy(S[0])
    k.LONG=S[0].LONG+b*v[0]
    k.LAT=S[0].LAT+b*v[1]
    di=d([P.LONG, P.LAT],[k.LONG, k.LAT])
    return di
   # print([di,S[0].IND,S[1].IND,P.IND])
    
def wn_InPoly(P,V,n):
    wn=0
    MIN_LONG=190
    MAX_LONG=-190
    MIN_LAT=93
    MAX_LAT=-93
    for v in V:
        if v.LAT>MAX_LAT:
            MAX_LAT=v.LAT
        if v.LAT<MIN_LAT:
            MIN_LAT=v.LAT
        if v.LONG>MAX_LONG:
            MAX_LONG=v.LONG
        if v.LONG<MIN_LONG:
            MIN_LONG=v.LONG
    if P.LAT<MIN_LAT or P.LONG<MIN_LONG or P.LAT>MAX_LAT or P.LONG>MAX_LONG:
        return False
    for i in range(n-1):
        
        #print(V[i].LAT,V[i].LONG)
        if V[i].LAT<=P.LAT:
            if V[i+1].LAT>P.LAT:
                if isLeft(P,V[i],V[i+1])>0:
                    wn+=1

        else:
            if (V[i+1].LAT<=P.LAT):
                if isLeft(P,V[i],V[i+1])<0:
                    wn-=1
    #print([P.IND,wn])
    if wn==0:
        return False
    return True
