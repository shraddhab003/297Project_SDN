import networkx as nx

G1 = nx.Graph()
G1.add_node(1)
G1.add_node(2)
G1.add_node(3)
G1.add_edges_from([(1,2),(2,3)])

G2 = nx.Graph()
G2.add_node(5)
G2.add_node(6)
G2.add_node(7)
G2.add_node(4)
G2.add_edges_from([(4,5),(5,6),(6,7)])

H=nx.union(G1,G2,rename=('a-','b-'))
elist=[ ('a-'+str(n1),'b-'+str(n1)) for n1 in G1 if n1 in G2]
H.add_edges_from(elist)
g1 = nx.shortest_path(G1,1,3)
print g1
g2 = nx.shortest_path(G2,4,7)
print g2
s = nx.shortest_path(H,1,7)
print s
