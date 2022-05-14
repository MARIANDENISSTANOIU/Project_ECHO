import math
import Geometrics
import numpy as np
def create_maze(BEGIN_COORDS,END_COORDS,ASP):
    #Defining classes to be used in the file (might be needed to be reworked and moved to antoher 'main' file)
    #Node Class. To be used in A* ()
    #Point Class: Points generated on the grid
    class Node():
    #"""A node class for A* Pathfinding"""
        def __init__(self,b,s=False,f=False):
            self.LAT=b.LAT
            self.LONG=b.LONG
            self.pos=(b.LONG,b.LAT)
            self.neighbours=b.neighbours
            self.parent=None
            self.g = float("inf")
            self.f = float("inf")
            self.IND=b.IND
            self.VALID=b.VALID
            self.isStart=s
            self.isFin=f
            self.isClosed=False
            self.isOpen=False
        def __lt__(self,other):
            return False
    maze=[]
    class Point():
        def __init__(self,LONG,LAT):
            self.LONG=LONG
            self.LAT=LAT
            self.IND=-2
            self.VALID=1 #Valid: can the point be accessed or is it in a restricted area?-might remove
            self.neighbours=[]
            #Valid directions (North, South, East, West aka UP,DOWN etc.; SW, NE, SE etc.)
    #ASP_POINT subclass of point. Used to define the vertexes of the enclosed airspace
    class ASP_POINT(Point):
            def __init__(self, LONG, LAT,ind):
                super().__init__(LONG, LAT)
                self.indx=ind
    def dist(P1,P2):
            return math.sqrt((P1.LONG-P2.LONG)*(P1.LONG-P2.LONG)+(P1.LAT-P2.LAT)*(P1.LAT-P2.LAT) )  
    BEGIN=Point(BEGIN_COORDS[0],BEGIN_COORDS[1])
    ENDING=Point(END_COORDS[0],END_COORDS[1])
    #Importing airspace

    #Creating Airspace Vertex points as ASP_POINT class
    ASP_POINTS=[]
    ind=1
    for vert in ASP.POINTS:
        p=ASP_POINT(vert[0],vert[1],vert[2])
        p.IND=ind
        ind+=1
        ASP_POINTS.append(p)
        pass
    #Creating the edges of the airspace as a list of pairs of points defining an edge
    AIRSPACE=[]
    
    for i in range(len(ASP_POINTS)-1):
     
        AIRSPACE.append([ASP_POINTS[i],ASP_POINTS[i+1]])
    AIRSPACE.append([ASP_POINTS[-1],ASP_POINTS[0]])
    
    #Final and last point Coordinates
    # for p in ASP_POINTS:
    #     print([p.LAT,p.LONG])
    #Defining the boundary box
    MIN_LONG=MAX_LONG=BEGIN_COORDS[0]
    MIN_LAT=MAX_LAT=BEGIN_COORDS[1]
    for i in ASP.POINTS:
        if i[0]>MAX_LONG:
            MAX_LONG=i[0]
        if i[0]<MIN_LONG:
            MIN_LONG=i[0]
        if i[1]>MAX_LAT:
            MAX_LAT=i[1]
        if i[1]<MIN_LAT:
            MIN_LAT=i[1]
    #We need to check if the airspace blocks all paths in the general
    #direction of the target point and if it does, we need to create 
    #a bigger grid
    
    MAX_LAT=max(MAX_LAT,END_COORDS[1])+6/60
    MIN_LAT=min(MIN_LAT,END_COORDS[1])-6/60
    MAX_LONG=max(MAX_LONG,END_COORDS[0])+6/60
    MIN_LONG=min(MIN_LONG,END_COORDS[0])-6/60
    m=abs(MAX_LONG-MIN_LONG)*60
    WIDTH=abs(MAX_LAT-MIN_LAT)*60
    BEGIN.IND=-1
    #generating the points on the grid and checking whether they are viable routing points
    #or if they are in the restricted area
    md3=md1=[999,0]
    md4=md2=[999,0]
    x1=1
    
    for i in np.arange(MIN_LONG,MAX_LONG,1/60):
        m=0
        # for da in ASP_POINTS:
        #         print([da.LAT,da.LONG])
        v=[]
        for j in np.arange(MIN_LAT,MAX_LAT,1/60):
            p=Point(i,j)
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
                    md2=[dist(p,ENDING),x1-1]
                    if md4[0]>md2[0]:
                        md4=md2
                        md2=[dist(p,BEGIN),x1-1]
                    else:
                        md2=[dist(p,BEGIN),x1-1]
            
            
            if ok:
                p.VALID=0    
           
            maze.append(Node(p))
            v.append(p.VALID)
            x1+=1
       # print(v)
    ENDING.IND=9999

    for i in range(len(maze)-2):
        if maze[i]==md1[1]:
            maze[i].neighbours.append(md1[1])
        if maze[i]==md2[1]:
            maze[i].neighbours.append(md2[1])
        
        if maze[i].LAT<MAX_LAT:
            if maze[i+1].VALID==1:
                maze[i].neighbours.append(maze[i+1])
        if maze[i].LAT>MIN_LAT:
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
        pass    
    BEGIN=Node(BEGIN,True,False)
    ENDING=Node(ENDING,False,True)
    BEGIN.neighbours=[maze[md1[1]]]
    BEGIN.neighbours.append(maze[md3[1]])
    ENDING.neighbours=[maze[md2[1]]]
    ENDING.neighbours.append(maze[md4[1]])
 
    maze[md2[1]].neighbours.append(ENDING)            
    maze[md4[1]].neighbours.append(ENDING)
    maze.append(BEGIN)
    maze.append(ENDING)  

    ok=False
    for p in [BEGIN,ENDING]:
        for k in range(len(AIRSPACE)):
             if Geometrics.p2seg(AIRSPACE[k],p)<5/60:
                    ok=True
                    break
            
        if Geometrics.wn_InPoly(p,ASP_POINTS,len(ASP_POINTS)):
                ok=True
    if ok:            
        return [maze,False]
    else:
        return [maze,True]