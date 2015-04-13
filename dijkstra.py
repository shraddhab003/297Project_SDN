# For creating a graph in networkx with json data
import json
import networkx as nx

#For plotting the graph and getting its image
import matplotlib.pyplot as plt
import matplotlib.pyplot as pylab

# Plot graph
def save_graph(graph,file_name):

    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.5
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
         
    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

if __name__ == '__main__':
	from networkx.readwrite import json_graph

	G = nx.Graph()
	G.add_node(0)
	G.add_node(1)
	G.add_node(2)
	G.add_node(3)
	G.add_node(4)
	G.add_node(5)

	G.add_edge(0, 1, weight=7)
	G.add_edge(0, 2, weight=3)
	G.add_edge(1, 3, weight=1)
	G.add_edge(2, 3, weight=2)
	G.add_edge(2, 4, weight=6)
	G.add_edge(3, 5, weight=4)
	G.add_edge(4, 5, weight=5)

	try:
    		n=nx.shortest_path(G,1,5)
    		print n
	except nx.NetworkXNoPath:
    		print 'No path'
	

	data = json_graph.node_link_data(G)
	# s = json.dumps(data)
	# print s

	# Open a file for writing
	out_file = open("graph.json","w")

	# Save the dictionary into this file
	# (the 'indent=4' is optional, but makes it more readable)
	json.dump(data, out_file, indent=4)                                    

	# Close the file
	out_file.close()

	# Save a visualization of created graph
	save_graph(G,"my_graph.png")


