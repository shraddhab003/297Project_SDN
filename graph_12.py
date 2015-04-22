import networkx as nx
from networkx.readwrite import json_graph

import matplotlib.pyplot as plt
import json

import pymongo
from pymongo import MongoClient

#creating graph G1
G1 = nx.Graph()
G1.add_node(1)
G1.add_node(2)
G1.add_node(3)
G1.add_node('router')
G1.add_edges_from([(1,2),(2,3),(1,'router')])

#creating graph G2
G2 = nx.Graph()
G2.add_node('a')
G2.add_node('b')
G2.add_node('c')
G2.add_node('router')
G2.add_edges_from([('a','b'),('b','c'),('a','router')])

#Plotting of graph G1 and G2
#only for understanding
pos1 = nx.spring_layout(G1)
nx.draw_networkx_nodes(G1, pos1, node_size=700)
nx.draw_networkx_edges(G1, pos1, width=3)
nx.draw_networkx_labels(G1, pos1, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('images/graph1.png')
plt.close()

pos2 = nx.spring_layout(G2)
nx.draw_networkx_nodes(G2, pos2, node_size=700)
nx.draw_networkx_edges(G2, pos2, width=3)
nx.draw_networkx_labels(G2, pos2, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('images/graph2.png')
plt.close()

#using the networkx.compose function to join 2 graphs with a single common node
H=nx.compose(G1,G2)
posh = nx.spring_layout(H)
nx.draw_networkx_nodes(H, posh, node_size=700)
nx.draw_networkx_edges(H, posh, width=3)
nx.draw_networkx_labels(H, posh, font_size=20, font_family='sans-serif')
plt.axis('on')
plt.savefig('images/compose_H.png')
plt.close()

#calculating shortest path SAMPLES
path_1 = nx.shortest_path(H,3,'c')
print path_1

path_2 = nx.shortest_path(H,1,'b')
print path_2

#Genrating JSON for the combined graph
json_file = open("json/final_network.json", "w")
json_data = json_graph.node_link_data(H)
data = json.dumps(json_data, json_file, indent=3)
json_file.close()

#Creating mongoDB client and database
client = MongoClient('localhost', 27017)
db = client.network_db
collection = db.graph_collection

#load json and insert
my_data = json.loads(data)
json_insert = collection.insert(my_data)

