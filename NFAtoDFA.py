class Node:
    def __init__(self, id: int, connections: dict): # connections = {input: [state1,state2,...], ...}
        self.id = id
        self.connections = connections
    
class NFA:
    def __init__(self, nodes: list, start: Node, accept: list, alphabet: list):
        self.nodes = nodes
        self.start = start
        self.accept = accept
        self.alphabet = alphabet
    
    def checkString(self, s: str) -> bool:
        return False
        
def crawlNodes():
    pass
    
def NFAtoDFA(graph: list):
    pass