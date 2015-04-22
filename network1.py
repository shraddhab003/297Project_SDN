#! /usr/local/bin/python
# -*- coding: utf-8 -*-

# Creating graphs in networkx and generating its json file
import json
import networkx as nx
from networkx.readwrite import json_graph

# For plotting the graph and getting its image
import matplotlib.pyplot as plt
import matplotlib.pyplot as pylab

# For connection with MongoDB
import pymongo
from pymongo import MongoClient


def save_graph(graph,file_name):

	plt.figure(num=None, figsize=(20, 20), dpi=80)
	plt.axis('off')
	fig = plt.figure(1)
	pos = nx.spring_layout(graph)
	# nx.draw(G,pos,node_color='b',node_size=50,with_labels=False)
    	nx.draw_networkx_nodes(graph,pos)
    	nx.draw_networkx_edges(graph,pos,width = 2.0,)
    	nx.draw_networkx_labels(graph,pos)

    	cut = 1
    	xmax = cut * max(xx for xx, yy in pos.values())
	ymax = cut * max(yy for xx, yy in pos.values())
	plt.xlim(-1, xmax)
    	plt.ylim(-1, ymax)

    	plt.savefig(file_name,bbox_inches="tight")
    	pylab.close()
    	del fig


if __name__ == '__main__':

        client = MongoClient('localhost', 27017)
        db = client.mydb
        collection = db.graph_collection

        # Creating a graph by taking input from user
	n = input("Enter the number of nodes in network: ")
	m = input("Enter the number of edges to be added from new node to the existing one: ")
        G = nx.generators.barabasi_albert_graph(n,m)
	

        # Calculating the shortest path between the nodes
	start = input("Enter the source node:")
	end = input("Enter the destiation node:")
	
	if ((0<=start<n) and (0<=end<n)):        
        	a = nx.shortest_path(G,start,end)
                print ('Avg shortest path from', start, 'to', end, 'is', nx.shortest_path_length(G,start,end), 'hops:')
		print a
	else:
        	print 'No path for the nodes entered'

        # creation of json object
        data = json_graph.node_link_data(G)
        s = json.dumps(data)
        # print s
	
	links = data['links']
	for i in range(0, (len(links))):
		links[i]['network'] = 1	
        
	# Open a file for writing
        out_file = open("network1_info.json","w")
        # Save the dictionary into this file
        # (the 'indent=4' is optional, but makes it more readable)
        json.dump(data, out_file, indent=4)
	json_info = json.loads(s)
        
	graph = collection.insert(json_info)
        
	# Close the file
        out_file.close()
	
        # Save a visualization of created graph
        save_graph(G,"network1_topology.png")

        client.close()

