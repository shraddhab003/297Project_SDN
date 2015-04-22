import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
G1.add_node(1)
G1.add_node(2)
G1.add_node(3)
G1.add_node('router')
G1.add_edges_from([(1,2),(2,3),(1,'router')])

G2 = nx.Graph()
G2.add_node('a')
G2.add_node('b')
G2.add_node('c')
G2.add_node('router')
G2.add_edges_from([('a','b'),('b','c'),('a','router')])

pos1 = nx.spring_layout(G1)
nx.draw_networkx_nodes(G1, pos1, node_size=700)
nx.draw_networkx_edges(G1, pos1, width=3)
nx.draw_networkx_labels(G1, pos1, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('graph1.png')
plt.close()

pos2 = nx.spring_layout(G2)
nx.draw_networkx_nodes(G2, pos2, node_size=700)
nx.draw_networkx_edges(G2, pos2, width=3)
nx.draw_networkx_labels(G2, pos2, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('graph2.png')
plt.close()

H=nx.compose(G1,G2)
posh = nx.spring_layout(H)
nx.draw_networkx_nodes(H, posh, node_size=700)
nx.draw_networkx_edges(H, posh, width=3)
nx.draw_networkx_labels(H, posh, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('compose_H.png')
plt.close()


path_1 = nx.shortest_path(H,3,'c')
print path_1

path_2 = nx.shortest_path(H,1,'b')
print path_2