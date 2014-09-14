# Mazes

# set up lists of strings to represent the four test mazes
smallMazeText = [line.strip() for line in open('smallMaze.txt').readlines()]
mediumMazeText = [line.strip() for line in open('mediumMaze.txt').readlines()]
largeMazeText = [line.strip() for line in open('largeMaze.txt').readlines()]
hugeMazeText = [line.strip() for line in open('hugeMaze.txt').readlines()]

class Maze:
    def __init__(self, mazeText):
        self.maze = mazeText
        self.height = len(mazeText)
        self.width = len(mazeText[0])
        for row in mazeText:
            if "S" in row:
                c = row.find("S")
                r = mazeText.index(row)
        self.start = (r, c)
        for row in mazeText:
            if "G" in row:
                c = row.find("G")
                r = mazeText.index(row)
        self.goal = (r, c)

    def isPassable(self, (r,c)):
        location = (r, c)
        if self.maze[location[0]][location[1]] == "#":
            return False
        else:
            return True
        
class MazeSearchNode:
    def __init__(self, maze, currentCell, parentNode):
        self.maze = maze
        self.currentCell = currentCell
        self.parentNode = parentNode

    def getChildren(self):
        (r, c) = self.currentCell
        children = []
        if r > 0:
            if self.maze.isPassable((r-1, c)):
                children.append(MazeSearchNode(self.maze, (r-1, c), self))
        if c > 0:
            if self.maze.isPassable((r, c-1)):
                children.append(MazeSearchNode(self.maze, (r, c-1), self))
        if c < self.maze.height-1:
            if self.maze.isPassable((r, c+1)):
                children.append(MazeSearchNode(self.maze, (r, c+1), self))
        if r < self.maze.width-1:
            if self.maze.isPassable((r+1, c)):
                children.append(MazeSearchNode(self.maze, (r+1, c), self))
        return children
                                
    def getPath(self):
        path = []
        node = self
        while node is not None:
            path = [node.currentCell] + path
            node = node.parentNode
        return path

def mazeSearch(maze):
        if maze.start == maze.goal:
            return [maze.start]
        else:
            agenda = [MazeSearchNode(maze, maze.start, None)]
            visited = [maze.start]
            while len(agenda) != 0:
                      parent = agenda.pop(0)
                      for child in parent.getChildren():
                          if child.currentCell == maze.goal:
                              return child.getPath()
                          elif not child.currentCell in visited:
                              agenda.append(child)
                              visited.append(child.currentCell)
            return None

