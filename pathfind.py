import math
from queue import PriorityQueue

def h(p1,p2):
    x1,y1=p1.pos
    x2,y2=p2.pos
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    
def reconstruct_path(came_from,current):
    path=[current]
    while current in came_from:
        current=came_from[current]
        path.append(current)
    return path
def astar(start, finish):
    start_node=start
    start_node.g=0
    end_node=finish
    start_node.f=h(start_node,end_node)
     # Initialize both open and closed list
    count=0
    open_set = PriorityQueue()
    open_set.put((0,count,start_node))
    came_from={}
    open_set_hash={start_node}
    while not open_set.empty():
        current=open_set.get()[2]
        open_set_hash.remove(current)
        if current.IND==end_node.IND:
            path=reconstruct_path(came_from,end_node)
            path.append(start_node)
            return path[::-1]
        for neighbour in current.neighbours:
            temp_g_score=current.g+h(current,neighbour)
            if temp_g_score<neighbour.g:
                came_from[neighbour]=current
                neighbour.g=temp_g_score
                neighbour.f=temp_g_score+h(neighbour,end_node)
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((neighbour.f,count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.isOpen=True
        if current!=start:
            current.isClosed=True
    return False
    # Add the start node
    
