This project is dedicated to a school project and its aim is to create a pathfinding algorithm which would simulate the avoidance of a Temporary Segregated Airspace (TSA).
The final version, if we go that far, would allow the user to select a series of airspaces to display and to choose one which is going to be needed to be avoided.
Main Libraries used: 
folium
PyQt5
branca
pandas
The app is split into 4 main parts:
1. Interface builder and initialiser, Main_P.py . In our current form, it creates the main interface and allows the user to select the main inputs for the algorithm.
2. grid_builder.py . Takes the input from the interface and generates a grid of points to cover the entry and exit points, as well as the TSA and then proceeds to label each point as a node in a graph and check which is valid and which is not
3. Geometrics: Gemoetric functions based on Daniel Sunday's Phd., "Practical Geometry Algorithms with C++ code". The C++ code has been obtained from https://geomalgorithms.com/ and translated into Python
5. Pathfind, which is essentially the implementation of the A* algorithm. 
Resources:
https://geomalgorithms.com/ -"Practical Geometry Algorithms with C++ code", Daniel Sunda Phd
https://www.youtube.com/watch?v=JtiK0DOeI4A&t=4669s Inspiration for the pathfinding algorithm. 
