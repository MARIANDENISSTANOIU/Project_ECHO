from turtle import color
import folium
import io
import sys
import json
from branca.element import Element
from PyQt5 import  QtCore, QtGui,QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import branca
import pandas as pd
import Airspace_handler as ash
import pathfind as ptf
import mapper as mp
# class Airspace():
#     def __init__(self,NAME,asp_file):
#         self.CODE=NAME
#         df=pd.read_csv(asp_file)
#         self.POINTS=df.values.tolist()
#         self.Points2=df.values.tolist()
#         k=1
#         for i in self.POINTS:
#             i[2]=k
#             k=k+1 
#         self.POINTS[-1][2]=1

#         max_long=self.POINTS[0][0]
#         min_long=self.POINTS[0][0]
#         max_lat=self.POINTS[0][1]
#         min_lat=self.POINTS[0][1]
#         for i in range(len(self.POINTS)):
#             if min_long>self.POINTS[i][0]:
#                 min_long=self.POINTS[i][0]
#             if max_long<self.POINTS[i][0]:
#                 max_long=self.POINTS[i][0]
#             if min_lat>self.POINTS[i][1]:
#                 min_lat=self.POINTS[i][1]
#             if max_lat<self.POINTS[i][1]:
#                 max_lat=self.POINTS[i][1]
#         self.BOUNDARY=[min_lat,min_long,max_lat,max_long]
#         self.EDGES=[self.POINTS[0:2]]
#         for i in range(1,len(self.POINTS)-1):
#             self.EDGES.append(self.POINTS[i:(i+2)])
#         self.CONTOUR=[]
#         for p in self.Points2:
#             self.CONTOUR.append([p[1],p[0]])
class WebEnginePage(QWebEnginePage):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
    def javaScriptConsoleMessage(self,level,msg,line,sourceID):
        
        self.parent.handle_button_data(msg)
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OurProject")
        self.setMinimumSize(1500,800)
        self.layout= QtWidgets.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("gridLayout")
        self.setLayout(self.layout)
        
        #DropDown Point selectors
        self.StartcomboBox = QtWidgets.QComboBox()
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.StartcomboBox.setFont(font)
        self.StartcomboBox.setObjectName("comboBox")
        self.layout.addWidget(self.StartcomboBox, 1, 0, 1, 1)        
        
        self.EndcomboBox = QtWidgets.QComboBox()
        self.EndcomboBox.setFont(font)
        self.EndcomboBox.setObjectName("comboBox_2")
        self.layout.addWidget(self.EndcomboBox, 1, 2, 1, 1)
        
            #Importing Waypoints Data
        
        df=pd.read_csv("WPTS_RO")
        df1=df.values.tolist()
            #create a dictionary data type for ease of access of the points later on
        self.dict1={df1[0][1]:[df1[0][4],df1[0][3],df1[0][2]]}
        self.dict2={df1[0][2]:[df1[0][4],df1[0][3]]}
        for d in df1:
            self.dict1[d[1]]=[d[4],d[3],d[2]]
            self.dict2[d[2]]=[d[4],d[3]]
            self.StartcomboBox.addItem(d[2])
            self.EndcomboBox.addItem(d[2])
            #Creating the self.MAP object which will be used to display data
        self.MAP=folium.Map(location=[df1[5][4],df1[5][3]],zoom_start=5,tiles='Stamen Terrain')
        #Adding the airspace
        correct_input,self.ASPs=ash.def_asp("RESTRICTED.csv")
        self.dictASP={self.ASPs[0].name:self.ASPs[0]}
        self.current_closed_airspace=self.ASPs[-1]
        for a in self.ASPs:
            self.dictASP[a.name]=a
            if a.type=='P':
                folium.Polygon(a.CONTOUR,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(self.MAP)
            if a.type=='C':
                folium.Circle(location=a.centroid,radius=a.rad*1852,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(self.MAP)
            c1=a.name+"TSAC"
            c2=str(d[1])+"WPTO"
            html=""" 
            <h1 style="font-size:80%">{val}</h1>
            <p>
            <button type="button" id={id1} onclick="console.log(id)" style="font-size:90%">Choose this Airspace</button><br>
            </p>
            
            """.format(id1=c1,val=a.name)
            iframe=branca.element.IFrame(html=html,width=200,height=100)
            popup=folium.Popup(iframe,max_width=500)
            folium.Marker(location=a.centroid,popup=popup,tooltip=a.name).add_to(self.MAP)
        
        self.MAP2=self.MAP
        
        for d in df1:
            c1=str(d[1])+"WPTB"
            c2=str(d[1])+"WPTE"
            html=""" 
            <h1 style="font-size:80%">{val}</h1>
            <p>
            <button type="button" id={id1} onclick="console.log(id)" style="font-size:90%">Start Point</button><br>
            <button type="button" id={id2} onclick="console.log(id)" style="font-size:90%">End Point</button><br>
            </p>
            
            """.format(id1=c1,id2=c2,val=d[2])
            iframe=branca.element.IFrame(html=html,width=200,height=100)
            popup=folium.Popup(iframe,max_width=500)
            folium.CircleMarker(location=[d[4],d[3]],popup=popup,radius=10,tooltip=d[2]).add_to(self.MAP)
        #Embedding the MAP object to the self.webView window of the APP
        self.webView=QWebEngineView()
        page=WebEnginePage(self)
        self.webView.setPage(page)
        self.webView.setMinimumSize(600,300)
        self.webView.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                                 QtWidgets.QSizePolicy.MinimumExpanding))
        self.layout.addWidget(self.webView, 0, 0, 1, 3)
        
        self.initialise_map(self.MAP)
       
    
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                                 QtWidgets.QSizePolicy.MinimumExpanding))
        self.layout.addWidget(self.tableWidget, 0, 3, 1, 1)
        
    #Buttons
        #Start button
        self.StartSim = QtWidgets.QPushButton()
        self.StartSim.setFont(font)
        self.StartSim.setObjectName("StartSim")
        self.StartSim.setText("StartSim")
        self.layout.addWidget(self.StartSim, 1, 1, 2, 1)
        self.StartSim.clicked.connect(self.start_function)
        
        #Reset Button
        self.Reset = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.Reset.setFont(font)
        self.Reset.setObjectName("Reset")
        self.Reset.setText("Reset")
        self.layout.addWidget(self.Reset, 3, 1, 1, 1)
        self.Reset.clicked.connect(self.reset_function)
        

        #Export Button
        self.ExportButton = QtWidgets.QPushButton()
        self.ExportButton.setFont(font)
        self.ExportButton.setObjectName("ExportButton")
        self.ExportButton.setText("ExportButton") 
        self.layout.addWidget(self.ExportButton, 3, 0, 1, 1)
        self.ExportButton.clicked.connect(self.export_function)
        #Test display label
        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layout.addWidget(self.label, 2, 2, 2, 1)
        self.memorised_path=False
    def initialise_map(self,MAP):
        data=io.BytesIO()
        MAP.save(data,close_file=False)
        
        self.webView.setHtml(data.getvalue().decode())
    #Graphical check function, to be deleted if the thing works fine
    def start_function(self):
            maze=mp.do_magic(self.dict2[self.StartcomboBox.currentText()],self.dict2[self.EndcomboBox.currentText()],self.current_closed_airspace)
            #self.fu(maze,self.dict2[self.StartcomboBox.currentText()],self.dict2[self.EndcomboBox.currentText()])
           # self.fu(maze,self.dict2[self.StartcomboBox.currentText()],self.dict2[self.EndcomboBox.currentText()],self.current_closed_airspace)
            data2=io.BytesIO()
            
            paths=ptf.astar(maze[0][-2],maze[0][-1])
            path=[]
            #print(paths)
            MAP2=folium.Map(location=[(maze[0][-2].LAT+maze[0][-1].LAT)/2,(maze[0][-2].LONG+maze[0][-1].LONG)/2],start_zoom=5,tiles='Stamen Terrain')
            if paths:
                #print([paths[-2].LAT,paths[-2].LONG,paths[-2].IND])
                #print([paths[-1].LAT,paths[-2].LONG,paths[-1].IND])
                for p in paths:
                    path.append([p.LAT,p.LONG])
                    folium.CircleMarker(location=[p.LAT,p.LONG],radius=8,color="blue").add_to(MAP2)
                folium.PolyLine(path,colour="magenta").add_to(MAP2)
            if self.current_closed_airspace.type=="P":
                folium.Polygon(self.current_closed_airspace.CONTOUR,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(MAP2)
            if self.current_closed_airspace.type=="C":
                folium.Circle(location=self.current_closed_airspace.centroid,radius=self.current_closed_airspace.rad*1852,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(MAP2)
            
        
            folium.Marker(location=self.dict2[self.StartcomboBox.currentText()]).add_to(MAP2)
            folium.Marker(location=self.dict2[self.EndcomboBox.currentText()]).add_to(MAP2)
            
            self.initialise_map(MAP2)
            self.memorised_path=path
    def reset_function(self):
        self.initialise_map(self.MAP)
        
    
    def export_function(self):
        if self.memorised_path:
            data=self.memorised_path
            
            df_memmo=pd.DataFrame(data,columns=['LAT','LONG'])
            folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
            df_memmo.to_csv(path_or_buf=str(folderpath)+"/base.csv")
        else:
            self.label.setText("No path found or no input")

        
    def handle_button_data(self,msg):
        if msg[-4:-1]=="WPT":
            
            if msg[-1]=="B":
                self.StartcomboBox.setCurrentText(self.dict1[int(msg[:-4])][2])
            elif msg[-1]=="E":
                self.EndcomboBox.setCurrentText(self.dict1[int(msg[:-4])][2])
        if msg[-4:-1]=="TSA":
            self.current_closed_airspace=self.dictASP[msg[:-4]]
            b=self.dictASP[msg[:-4]]
            self.label.selectedText=msg[:-4]
    def fu(self,maze,BEGIN,END,ASP):
        if maze[1]==False:
            self.label.setText("Invalid Points. Select other")
        color_dict={1:'blue',
                    0:'pink'
                    }
        MAP=folium.Map(location=[45.6,26],start_zoom=5,tiles='Stamen Terrain')
        for p in maze[0]:
            folium.Circle(location=[p.LAT,p.LONG],radius=100,color=color_dict[p.VALID]).add_to(MAP)
        folium.CircleMarker(location=[maze[0][-2].LAT,maze[0][-2].LONG],tooltip="BEGIN",color="magenta",radius=12).add_to(MAP)
        folium.CircleMarker(location=[maze[0][-1].LAT,maze[0][-1].LONG],tooltip="END",color="green",radius=12).add_to(MAP)
        for p in maze[0][-1].neighbours:
            folium.PolyLine([[maze[0][-1].LAT,maze[0][-1].LONG],[p.LAT,p.LONG]],color="blue").add_to(MAP)
            folium.CircleMarker(location=[p.LAT,p.LONG],radius=12,color="yellow").add_to(MAP)
        for p in maze[0][-2].neighbours:
            folium.PolyLine([[maze[0][-2].LAT,maze[0][-2].LONG],[p.LAT,p.LONG]],color="pink").add_to(MAP)
            folium.CircleMarker(location=[p.LAT,p.LONG],color="black",radius=12).add_to(MAP)
        if ASP.type=="P":
            folium.Polygon(ASP.CONTOUR,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(MAP)
        if ASP.type=="C":
            folium.Circle(location=ASP.centroid,radius=ASP.rad*1852,color="black",weight=5,fill_color="red",fill_opacity=0.4).add_to(MAP)
        MAP.save("MAP2.html")
        
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())