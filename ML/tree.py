import matplotlib.pyplot as plt
import networkx as nx
import json

# Load your JSON data
data = {
    "root":{
        "child": ["HR", "IT", "Finance", "Customer Service"],
        "is_leaf": 0
    },
    "HR":{
        "child": ["Talent aquisition", "Diversity, Equity, and Inclusion"],
        "is_leaf": 0
    },
    "IT":{
        "child": ["Software Development", "Security"],
        "is_leaf": 0
    },
    "Finance":{
        "child": ["Accounting", "Treasury"],
        "is_leaf": 0
    },
    "Customer Service":{
        "child": ["alice@gmail.com", "bob@gmail.com"],
        "is_leaf": 1
    },
    "Talent aquisition":{
        "child": ["charlie@gmail.com", "dede@gmail.com"],
        "is_leaf": 0
    },
    "Diversity, Equity, and Inclusion":{
        "child": ["iliza@gmail.com", "jake@gmail.com"],
        "is_leaf": 1
    },
    "Software Development":{
        "child": ["kriss@gmail.com", "lana@gmail.com"],
        "is_leaf": 1
    },
    "Security":{
        "child": ["merry@gmail.com", "nina@gmail.com"],
        "is_leaf": 1
    },
    "Accounting":{
        "child": ["george@gmail.com", "harry@gmail.com"],
        "is_leaf": 1
    },
    "Treasury":{
        "child": ["eran@gmail.com", "ferb@gmail.com"],
        "is_leaf": 1
    }
}

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph
for parent, info in data.items():
    for child in info["child"]:
        G.add_edge(parent, child)

def hierarchy_pos(G, root=None, width=2., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=2., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None, parsed = []):
    if pos is None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children)!=0:
        dx = width/len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, parent = root, parsed=parsed)
    return pos


plt.figure(figsize=(35, 10))
pos = hierarchy_pos(G, 'root')
nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', width=2)
plt.savefig('tree.png')
plt.show()