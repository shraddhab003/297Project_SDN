#! /usr/local/bin/python
# -*- coding: utf-8 -*-

# For mininet topology
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host
from mininet.node import OVSKernelSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

import random
from networkx.generators.classic import empty_graph

from collections import defaultdict

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



def MyNetwork():
    net= Mininet(topo=None, build=False , ipBase='10.0.0.0/8' , link=TCLink)

    info("****Adding POX  Controller1****")

    poxController = net.addController(name='poxController' ,
                                 controller=RemoteController ,
                                 ip='10.0.2.15',
                                 port=6633)
    info("****Adding Second Controller")
    #poxController2 = net.addController(name='poxController2',
     #                                  controller=RemoteController ,
      #                                 ip='192.168.56.102' ,
       #                                port=6633)

    info('****Now Adding Two Switches')
    switch12=net.addSwitch('switch12')
    switch1=net.addSwitch('switch1')
    switch2=net.addSwitch('switch2')

    host1=net.addHost('h1', ip='10.0.0.1/8')
    host2=net.addHost('h2', ip='10.0.0.2/8')

    net.addLink(switch12,switch1)
    net.addLink(switch12,switch2)
    net.addLink(host1,switch1)
    net.addLink(host2,switch2)

    net.build()

    for controller in net.controllers:
        controller.start()

    net.get('switch1').start([poxController])
    #net.get('switch2').start([poxController2])
    #net.get('switch12').start([poxController])

    CLI(net)
    net.stop()

def _random_subset(seq,m):
    """ Return m unique elements from seq.

    This differs from random.sample which can return repeated
    elements if seq holds repeated elements.
    """
    targets=set()
    while len(targets)<m:
        x=random.choice(seq)
        targets.add(x)
    return targets

def barabasi_albert_graph(n, m, seed=None):
    """Return random graph using Barabási-Albert preferential attachment model.
        
    A graph of n nodes is grown by attaching new nodes each with m
    edges that are preferentially attached to existing nodes with high
    degree.
    
    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    seed : int, optional
        Seed for random number generator (default=None).   
    """
        
    if m < 1 or  m >=n:
        raise nx.NetworkXError(\
              "Barabási-Albert network must have m>=1 and m<n, m=%d,n=%d"%(m,n))
    if seed is not None:
        random.seed(seed)    

    # Add m initial nodes (m0 in barabasi-speak) 
    G=empty_graph(m)
    G.name="barabasi_albert_graph(%s,%s)"%(n,m)
    # Target nodes for new edges
    targets=list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge 
    repeated_nodes=[]     
    # Start adding the other n-m nodes. The first node is m.
    source=m 
    while source<n: 
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source]*m,targets)) 
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source]*m) 
        # Now choose m unique nodes from the existing nodes 
        # Pick uniformly from repeated_nodes (preferential attachement) 
        targets = _random_subset(repeated_nodes,m)
        source += 1
    return G

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
        G = nx.barabasi_albert_graph(n,m)
	

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

