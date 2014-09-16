class PriorityQueue:
    def __init__(self):
        self.data = []
    def push(self, item, cost):
        self.data.append((cost, item))
    def pop(self):
        (index, cost) = util.argmaxIndex(self.data, lambda (c, x): -c)
        return self.data.pop(index)[1] # just return the data item
    def isEmpty(self):
        return self.data is []

class SearchNode:
    def __init__(self, state, parent=None, cost=1):
        self.state = state
        self.parent = parent
        self.cost = cost

    def getPath(self):
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        return path[::-1]

    def getChildren(self, width, height):
        x, y = self.state
        children = []
        for(dx, dy) in [(1,0), (0,1), (-1,0), (0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nx, ny = x+dx, y+dy
            if nx > 0 and ny > 0 and nx < width and ny < height:
                out.append(SearchNode((nx,ny), self))
        return children

class BadLocations:
    badlocs = []

    def isBadLoc(position):
        return position in badlocs

    def addBadLoc(position):
        badlocs.append(position)


def search(init, goal, dfs=False):
    if init == goal:
        return [init]
    else:
        agenda = [SearchNode(init)]
        visited = set(init)
        while len(agenda):
            #BFS uses a queue, DFS uses a stack
            node = agenda.pop(0) if not dfs else agenda.pop()
            if node.state not in visited:
                visited.add(node.state)
                if node.state == goal:
                    return node.getPath()
                for child in node.getChildren():
                    if child.state not in visited and not BadLocations.isBadLoc(child.state):
                        agenda.append(child)
    return None

import sys

def all_points(start, end, grid_width, grid_height):
    points = [start, end]
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

def dijkstra(init, goal, grid):
    def euclidean(a,b):
        x1, y1 = a.state
        x2, y2 = b.state
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

    # Source -> source distance = 0
    dist = {tuple(init): 0}
    previous = {}
    
    for point in grid:
        dist[point] = float("inf")

    pq = PriorityQueue()

    while not pq.isEmpty():
        u = pq.pop()
        for child in u:
            d = dist[tuple(u.state)] + euclidean(u, child)
            if d < dist[tuple(v.state)]:
                dist[tuple(v.state)] = d
                previous[tuple(v.state)] = u
    return dist, previous

def ucSearch(init, goal, heuristic=lambda s: 0):
    if init == goal:
        return [init]
    else:
        agenda = [ (SearchNode(init), init.cost + heuristic(init.state)) ]
        visited = set(init)
        while len(agenda):
            agenda.sort(key=lambda n: n[1])
            node, cost = agenda.pop(0)
            if node.state not in visited:
                visited.add(node.state)
                if node.state == goal:
                    return node.getPath()
                for child in node.getChildren():
                    if child.state not in visited:
                        agenda.append( (child, child.cost + heuristic(child.state ) ))
    return None