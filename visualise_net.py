from pyvis.network import Network
from import_data import fetch_structure_data
import itertools

nodes_, links_, demands_ = fetch_structure_data("polska.xml")

# # creating graph of nodes
# net = Network()
# for i in range(len(nodes_)):
#     net.add_node(i, label=nodes_[i])
    
# nodes_ids = range(len(nodes_))
# edges = itertools.combinations(nodes_ids, 2)
# for edge in edges:
#     net.add_edge(edge[0], edge[1])

# net.show('net.html')

gb_net = Network()
gb_net.add_node(0, label="Gdańsk", mass=5)
gb_net.add_node(2, label="Kołobrzeg", mass=5)
gb_net.add_node(1, label="Bydgoszcz", mass=5)
gb_net.add_node(10, label="Warszawa", mass=5)
gb_net.add_node(9, label="Szczecin", mass=5)
gb_net.add_node(7, label="Poznań", mass=5)

gb_net.add_edge(0, 2, label="Link_0_2", color='purple', width=10)
gb_net.add_edge(0, 10, label="Link_0_10", color='green', width=5)
gb_net.add_edge(1, 2, label="Link_1_2", color='blue', width=5)
gb_net.add_edge(1, 10, label="Link_1_10", color='green', width=5)
gb_net.add_edge(2, 9, label="Link_2_9", color='red', width=5)
gb_net.add_edge(7, 9, label="Link_7_9", color='red', width=5)
gb_net.add_edge(7, 1, label="Link_7_1", color='red', width=5)

gb_net.show('net.html')
