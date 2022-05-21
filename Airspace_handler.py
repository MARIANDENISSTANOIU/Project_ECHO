from numpy import double
import pandas as pd
import json
import os
class Airspace():
    def __init__(self,NAME,VTX,type):
        self.name=NAME
        self.type="P"
        self.POINTS=VTX
        self.centroid=self.define_centroid()
        self.Points2=VTX
        k=1
        # print("MY ASP")
        # print(self.POINTS)
        
        for i in self.POINTS:
            i.append(k)
            k=k+1 
        self.POINTS[-1][2]=1
       
        max_long=self.POINTS[0][1]
        min_long=self.POINTS[0][1]
        max_lat=self.POINTS[0][0]
        min_lat=self.POINTS[0][0]
        for i in range(len(self.POINTS)):
            if min_long>self.POINTS[i][1]:
                min_long=self.POINTS[i][1]
            if max_long<self.POINTS[i][1]:
                max_long=self.POINTS[i][1]
            if min_lat>self.POINTS[i][0]:
                min_lat=self.POINTS[i][0]
            if max_lat<self.POINTS[i][0]:
                max_lat=self.POINTS[i][0]
        self.BOUNDARY=[min_lat,min_long,max_lat,max_long]
        self.EDGES=[self.POINTS[0:2]]
        for i in range(1,len(self.POINTS)-1):
            self.EDGES.append(self.POINTS[i:(i+2)])
        self.CONTOUR=[]
        for p in self.Points2:
            self.CONTOUR.append([p[0],p[1]])
    def define_centroid(self):
        k=0
        lc=0.0
        lonc=0.0
        for i in self.POINTS:
            lc=i[0]+lc
            k=k+1
            lonc=i[1]+lonc
        lc=lc/k
        lonc=lonc/k
        return [lc,lonc]                
class Circle_Airspace():
    def __init__(self,name,type,lat_c,long_c,rad):
        self.name=name
        self.type="C"
        self.centroid=[lat_c,long_c]
        self.rad=rad
        self.BOUNDARY=[lat_c-rad/60,long_c-rad/60,lat_c+rad/60,long_c+rad/60]
def def_asp(filename):
    file_name, file_extension = os.path.splitext(filename)
    AIRSPACES=[]
    if file_extension==".csv":
 #       print("It IS")
        df=pd.read_csv(filename,sep=';')
    df1=df.values.tolist()
    #print(df1)
    for i in df1:
        if i[1]=='C':
            #print([i[2][0:8],i[2][9:18],i[2][-1]])    
            lat_c=double(i[2][0:8])
            long_c=double(i[2][9:18])
            rad=double(i[2][19:])
            AIRSPACES.append(Circle_Airspace(i[0],i[1],lat_c,long_c,rad))
        if i[1]=='P':
            b=i[2].split('#')
            VTX=[]
            #print(b)
            for j in b:
                pass
                c=j.split(',')
                VTX.append([double(c[0]),double(c[1])])
            d=Airspace(i[0],VTX,i[1])
            AIRSPACES.append(d)
    return (False,AIRSPACES)
#def_asp("RESTRICTED.csv")
# b="46.4335374248444,21.82706562855166#46.44967022285501,21.73143668083187#46.2845557003399,21.56814417224279#46.26639654895123,21.81187026199319#46.4335374248444,21.82706562855166"
# c=b.split('#')
# print(c)
# d=c[0].split(',')
# print(d)