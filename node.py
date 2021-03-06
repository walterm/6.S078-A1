def getNeighbors(point, grid_size):
    x, y = point
    children = []
    for(dx, dy) in [(1,0), (0,1), (-1,0), (0,-1)]:
        nx, ny = x+dx, y+dy
        if nx >= 0 and ny >= 0 and nx < grid_size and ny < grid_size:
            children.append((nx,ny))
    return children       

from Queue import PriorityQueue

class SearchNode:
    def __init__(self, state, parent=None, cost=1):
        self.state = tuple(state)
        self.parent = parent
        self.cost = cost

    def getPath(self):
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        return path[::-1]

    def getChildren(self):
        grid_size = 50
        x, y = self.state
        children = []
        for(dx, dy) in [(1,0), (0,1), (-1,0), (0,-1)]:
            nx, ny = x+dx, y+dy
            if nx >= 0 and ny >= 0 and nx < grid_size and ny < grid_size:
                children.append(SearchNode((nx,ny), self))
        return children

class BadLocations:
    badlocs = set()

    @classmethod
    def isBadLoc(cls,position):
        return tuple(position) in cls.badlocs

    @classmethod
    def addBadLoc(cls,position):        
        cls.badlocs.add(tuple(position))


def __goalTest(test, goal):
    return goal[0] == test[0] and goal[1] == test[1]

def search(init, goal, dfs=False):

    if __goalTest(init, goal):
        return [init]
    else:
        agenda = [SearchNode(init)]
        visited = set( init )
        while len(agenda) != 0:
            #BFS uses a queue, DFS uses a stack
            if dfs:
                node = agenda.pop()
            else:
                node = agenda.pop(0)
            node.state = tuple(node.state)
            if node.state not in visited:
                visited.add(node.state)
                if __goalTest(goal, node.state):
                    return node.getPath()
                for child in node.getChildren():
                    child.state = tuple(child.state)
                    if child.state not in visited and not BadLocations.isBadLoc(child.state):
                        agenda.append(child)
    return None

import sys

def all_points(start, grid_width, grid_height):
    points = [start]
    seen_points = set()
    while len(points) != 0:
        x, y = points.pop(0)
        for(dx, dy) in [(1,0), (0,1), (-1,0), (0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nx, ny = x+dx, y+dy
            if nx >= 0 and ny >= 0 and nx < grid_width and ny < grid_height:
                new_point = (nx, ny)
                if new_point not in seen_points:
                    seen_points.add(tuple( (nx, ny) ) )
                    points.append([nx,ny])
    return seen_points

def euclidean(a,b):
    x1, y1 = a
    x2, y2 = b
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

def dijkstra(init, goal, grid, grid_size=10):
    dist = {point: float('inf') for point in grid}
    previous = {point: None for point in grid}
    dist[tuple(init)] = 0
    q = grid.copy()
    neighbors = {point: set() for point in grid}
    for point in grid:
        for neighbor in getNeighbors(point, grid_size):
            neighbors[point].add( (neighbor, euclidean(point, neighbor)) )
    while q:
        u = min(q, key=lambda vertex: dist[vertex])
        q.remove(u)
        if dist[u] == float('inf') or u is init:
            break
        for v, cost in neighbors[u]:
            d = dist[u] + cost
            if d < dist[v]:
                dist[v] = d
                previous[v] = u
    s, u = [], tuple(goal)
    while previous[u]:
        s.insert(0, u)
        u = previous[u]
    s.insert(0, u)
    return s


def ucSearch(init, goal, heuristic=lambda s: 0):
    if init == goal:
        return [init]
    else:
        agenda = [ (SearchNode(init), 0) ]
        visited = set(SearchNode(init).state)
        while len(agenda):
            agenda.sort(key=lambda n: n[1])
            node, cost = agenda.pop(0)
            if node.state not in visited:
                visited.add(node.state)
                if __goalTest(goal, node.state):
                    return node.getPath()
                for child in node.getChildren():
                    if child.state not in visited and not BadLocations.isBadLoc(child.state):
                        agenda.append( (child, child.cost + heuristic(child.state ) ))
    return None

if __name__ == "__main__":
    goal = [7, 7]
    heuristic = lambda x: 3 * ((x[0] - goal[0]) ** 2 + (x[1] - goal[1]) ** 2)
    print ucSearch([0,0], goal, heuristic)
