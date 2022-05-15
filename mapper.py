import math
import Geometrics
import numpy as np
class Node():
    def __init__(self,LAT,LONG,IND=False,start=False,fin=False) :
        self.LAT=LAT
        self.LONG=LONG
        self.pos=[self.LAT,self.LONG]
        self.IND=-2
        self.VALID=1 #Valid: can the point be accessed or is it in a restricted area?-might remove
        self.neighbours=[]
        self.parent=None
        self.g = float("inf")
        self.f = float("inf")
        self.isStart=start
        self.isFin=fin
        self.isClosed=False
        self.isOpen=False
class ASP_POINT():
    def __init__(self, LONG, LAT,ind):
        self.LONG=LONG
        self.LAT=LAT
        self.indx=ind
def dist(P1,P2):
            return math.sqrt((P1.LONG-P2.LONG)*(P1.LONG-P2.LONG)+(P1.LAT-P2.LAT)*(P1.LAT-P2.LAT) )
def do_magic(BEGIN_COORDS,END_COORDS,ASP):
    BEGIN=Node(BEGIN_COORDS[0],BEGIN_COORDS[1],start=True)
    ENDING=Node(END_COORDS[0],END_COORDS[1],fin=True)
    ASP_POINTS=[]
    ind=1
    for vert in ASP.POINTS:
        p=ASP_POINT(vert[0],vert[1],ind)
        p.IND=ind
        ind+=1
        ASP_POINTS.append(p)
    AIRSPACE=[]
    
    for i in range(len(ASP_POINTS)-1):
     
        AIRSPACE.append([ASP_POINTS[i],ASP_POINTS[i+1]])
    AIRSPACE.append([ASP_POINTS[-1],ASP_POINTS[0]])
    ok=False
    for p in [BEGIN,ENDING]:
        for k in range(len(AIRSPACE)):
             if Geometrics.p2seg(AIRSPACE[k],p)<5/60:
                    ok=True
                    break
            
        if Geometrics.wn_InPoly(p,ASP_POINTS,len(ASP_POINTS)):
                ok=True
                break
    MAX_LAT=max(ASP.BOUNDARY[2],BEGIN_COORDS[0],END_COORDS[0])+6/60
    MIN_LAT=min(ASP.BOUNDARY[0],BEGIN_COORDS[0],END_COORDS[0])-6/60
    MAX_LONG=max(ASP.BOUNDARY[3],BEGIN_COORDS[1],END_COORDS[1])+6/60
    MIN_LONG=min(ASP.BOUNDARY[1],BEGIN_COORDS[1],END_COORDS[1])-6/60
    print([MIN_LAT,MIN_LONG])
    print([MAX_LAT,MAX_LONG])

    BEGIN.IND=-1
    md3=md1=[999,0]
    md4=md2=[999,0]
    x1=1
    maze=[]
    for i in np.arange(MIN_LONG,MAX_LONG,1/60):
        m=0
        # for da in ASP_POINTS:
        #         print([da.LAT,da.LONG])
        v=[]
        for j in np.arange(MIN_LAT,MAX_LAT,1/60):
            p=Node(j,i)
        #We need to check if the point is Valid or not 
            
            ok=False
            m+=1
            p.IND=x1
            #checks the point p with every edge of the ASP to see if it's closer than 5NM
            for k in range(len(AIRSPACE)):
                if Geometrics.p2seg(AIRSPACE[k],p)<5/60:
                    ok=True
                    break
            
            if Geometrics.wn_InPoly(p,ASP_POINTS,len(ASP_POINTS)):
                ok=True
             # Which are the closest 2 neighbours of STAR/BEGIN nodes and ENDING node   
            if md1[0]>dist(p,BEGIN) and p.VALID!=0:
                    if md3[0]>md1[0]:
                        md3=md1
                        md1=[dist(p,BEGIN),x1-1]
                    else:
                        md1=[dist(p,BEGIN),x1-1]
            if md2[0]>dist(p,ENDING) and  p.VALID!=0:
                    if md4[0]>md2[0]:
                        md4=md2
                        md2=[dist(p,ENDING),x1-1]
                    else:
                        md2=[dist(p,ENDING),x1-1]
            
            
            if ok:
                p.VALID=0    
           
            maze.append(p)
            v.append(p.VALID)
            x1+=1
       # print(v)
    ENDING.IND=-2
    for i in range(len(maze)-1):
       
        # if maze[i]==md1[1]:
        #     maze[i].neighbours.append(md1[1])
        # if maze[i]==md2[1]:
        #     maze[i].neighbours.append(md2[1])
        
        if maze[i+1].LAT<MAX_LAT:
            if maze[i+1].VALID==1:
                maze[i].neighbours.append(maze[i+1])
        if maze[i-1].LAT>MIN_LAT:
            if maze[i-1].VALID==1:
                maze[i].neighbours.append(maze[i-1])
        if i-m>0 and maze[i-m].VALID==1:
            maze[i].neighbours.append(maze[i-m])
        if i-m-1>0:
            if maze[i-m-1].LAT<MAX_LAT and maze[i-m-1].VALID==1:
                maze[i].neighbours.append(maze[i-m-1])
        if i-m+1>0:
            if maze[i-m+1].LAT>MIN_LAT and maze[i-m+1].VALID==1:
                maze[i].neighbours.append(maze[i-m+1])        
        if i+m<x1-1 and maze[i+m].VALID==1:
            maze[i].neighbours.append(maze[i+m])
        if i+m-1<x1-1:
            if maze[i+m-1].LAT>MIN_LAT and maze[i+m-1].VALID==1:
              maze[i].neighbours.append(maze[i+m-1])
        if i+m+1<x1-1:
            if maze[i+m+1].LAT<MAX_LAT and maze[i+m+1].VALID==1:
                maze[i].neighbours.append(maze[i+m+1])
    BEGIN.neighbours=[maze[md1[1]]]
    BEGIN.neighbours.append(maze[md3[1]])
    ENDING.neighbours=[maze[md2[1]]]
    ENDING.neighbours.append(maze[md4[1]])
    
    maze[md3[1]].neighbours.append(BEGIN)            
    maze[md1[1]].neighbours.append(BEGIN)
    
    maze[md2[1]].neighbours.append(ENDING)            
    maze[md4[1]].neighbours.append(ENDING)
    maze.append(BEGIN)
    maze.append(ENDING) 
    if ok:            
        return [maze,False]
    else:
        return [maze,True]