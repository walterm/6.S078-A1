class SearchNode:
    def __init__(self,state,parent,cost):
        self.state = state
        self.parent = parent
        self.cost = cost

    def getChildren(self):
        pass # application dependent

    def getPath(self):
        path = []
        current = self
        while current is not None:
            path = [current.state]+path
            current = current.parent
        return path

def ucSearch(startNode, goalTest, heuristic=lambda s: 0):
    if goalTest(startNode.state):
        return startNode.getPath()
    agenda = [(startNode,startNode.cost+heuristic(startNode.state))]
    expanded = set()
    while len(agenda) > 0:
        agenda.sort(key=lambda n: n[1])
        node,priority = agenda.pop(0)
        if node.state not in expanded:
            expanded.add(node.state)
            if len(expanded)%1000==0: print "Expanded",len(expanded),"states"
            if goalTest(node.state):
                print "Expanded",len(expanded),"states"
                return node.getPath()
            for child in node.getChildren():
                if child.state not in expanded:
                    agenda.append((child,child.cost+heuristic(child.state)))
    print "Expanded",len(expanded),"states"
    return None

class PuzzleSearchNode(SearchNode):
    def getChildren(self):
        pass # your code here

