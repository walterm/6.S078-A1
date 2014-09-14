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
        for(dx, dy) in [(1,0), (0,1), (-1,0), (0-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nx, ny = x+dx, y+dy
            if nx > 0 and ny > 0 and nx < width and ny < height:
                out.append(SearchNode((nx,ny), self, self.cost+1.0))
        return children

def searc(init, goal, dfs=False):
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
                    if child.state not in visited:
                        agenda.append(child)
    return None
