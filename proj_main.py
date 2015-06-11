#! /usr/local/bin/python
# -*- coding: utf-8 -*-

import random

import networkx as nx
from networkx.readwrite import json_graph

import matplotlib.pyplot as plt
import json

import pymongo
from pymongo import MongoClient
#from mongo import connect as PyConnection
from bson.objectid import ObjectId

import time

def create_graph(subnw_no):
	print ('Creating a graph.....')
	# subnw_no = input ('Enter the Sub-network: ')
	n = input('Enter the no. of nodes for network '+ str(subnw_no) + ':')
	m = input ('Enter the edges to be added from new node to the existing one: ')
	G = nx.generators.barabasi_albert_graph(n,m)
	G.add_node('router')
	r = random.randrange(0,n)
	G.add_edge(r,'router')	
	print 'Sub-network', subnw_no, 'is created with', n , 'nodes'
	return G

def mapping(graph,subnw_no,mapper):
	new_dict = {x: mapper + str(x) for x in range(0,len(graph) - 1)}
	G=nx.relabel_nodes(graph,new_dict, copy=False)
	return G
	
def generate_json(graph,subnw_no):
	# Generating json object and creating a json file for sub-network1
	json_data = json_graph.node_link_data(graph)
	# nodes = json_data['nodes']
	# for i in range(0, (len(nodes) - 1)):
	#	if nodes[i]['id'] == 'router' :
	#		pass
	#	else:
	#		nodes[i]['network'] = subnw_no
	json_data['network'] = subnw_no
	json_file = open("json/sub_network" + str(subnw_no) + ".json","w")
	data = json.dump(json_data, json_file, indent=4)
	json_file.close()
	if (len(json_data) > 0):
		print 'JSON information for Graph ' + str(subnw_no) +  ' inserted in a file successfully.'
		return json_data
	else :
		print 'JSON information insertion unsuccessful.'

	
def create_figure(graph,subnw_no,path):
	pos = nx.spring_layout(graph)
	'''
	for n in graph.nodes():
		if n in path :
			node_colors = ["blue"]
		else:
			node_colors = ["red"]
	'''
	node_colors = ["blue" if n in path else "red" for n in graph.nodes()]
	if subnw_no == 4 :	
		nx.draw_networkx_nodes(graph, pos, node_size=500, node_color = node_colors)
		nx.draw_networkx_edges(graph, pos, width=2)
		nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')
	else :
		nx.draw_networkx_nodes(graph, pos, node_size=500)
                nx.draw_networkx_edges(graph, pos, width=2)
                nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')
	plt.axis('on')
	plt.savefig('images/graph' + str(subnw_no) + '.png')
	plt.close()

def mongodb_client():
	client = MongoClient('localhost', 27017)
	# db = client.mydb
	# collection = db.graph_collection	
	print'MongoDB client connected to the server'
	return client

def insert_mongodb(json_data):
	# db = client.mydb
	# client = mongodb_client()
	db = client.mydb
	collection = db.graph_collection
	# json_data = json_graph.node_link_data(graph)	
	s = json.dumps(json_data)
	json_info = json.loads(s)
	graph_id = collection.insert(json_info)
	# client.close()
	if (graph_id > 0):
		print 'Graph information inserted in database successfully with id : ' + str(graph_id)
      		#list_graphs.append(str(graph_id))
                return graph_id
	else :
		print 'Graph information insertion unsuccessful.'

def insert_node(graph,subnw_no):
	# sub_nw = input('Enter which subnetwork to be changed: ')
	new_node = input('Enter the new node to be inserted: ')
	ex_no = input('Enter the existing node no. to be attached to the new node: ')
	graph.add_node(new_node)
	G.add_edge(ex_no, new_node)
	return G

def shortestpath(graph):
	src = raw_input('Enter the source: ')
	dest = raw_input('Enter the destination: ')
	
	#src = tempsrc.decode('utf-8')
	#dest = tempdest.decode('utf-8')
	s = unicode(src)
	# print s
	#dest = 'u' + str("'") + str(d) + str("'")
	d = unicode(dest)
	# print d
	
	path = nx.shortest_path(graph,s,d)
	return path
	# print path[src][dest]
	# print 'The shortest path from ' + str(s) + ' to ' + str(d) + ' is: ' + str(pat)h

def retrieve_db(subnw_no_edit):
	# client = mongodb_client()
        db = client.mydb
        collection = db.graph_collection
	l = subnw_no_edit - 1
	data_graph = collection.find({"_id" :ObjectId(list_graphs[l])})
       	for temp in data_graph:
		return temp
	# return data_graph

def check_node(graph,edge_add):
	chk_n = graph.has_node(edge_add)
	if chk_n == True :
		return 1
	else:
		return 0

def remove_mongodb_doc(subnw_no_ed):
	# client = mongodb_client()
        db = client.mydb
        collection = db.graph_collection
	l = subnw_no_edit - 1
	remove_data = collection.remove({'_id':ObjectId(list_graphs[l])})
	# src = filter(str.isdigit,str(edge_node))
	# tar = filter(str.isdigit,str(new_node))
	# update_data = collection.update({'_id':ObjectId(list_graphs[l])}, {'$push': {'nodes' : {'id': (new_node)},'links' : {'source' : (int(src) - 1) , 'target' : (int(tar) - 1)}}})
def remove_mongodb():
	# client = mongodb_client()
        db = client.mydb
        collection = db.graph_collection
	# c = Connection('localhost', 27017)
	db.drop_collection("graph_collection")
	# db.drop_collection("graph_collection")
	# client.close()
	
	
if __name__ == '__main__':
	print('*************HANDLING SCALABILITY IN SDN*************')
	condition = "Y"
	list_graphs = []
	check_err = 0
	path = []
	client = mongodb_client()
	while condition == "Y":
		i = input('Enter the operation to be performed: 1. create a new graph 2.Inserting a node in the existing graph: ')
		# list_graphs = []
		if i == 1 :
			# no_graphs = input('Enter number of graphs to be created: ')
			# list_graphs = []
			remove_mongodb()
			path = []
			list_graphs = []
			for x in range(0,3):
				print ('******************************************************************************************************')
				subnw_no = input ('Enter the Sub-network: ')
				# n1 = input('Enter the no. of nodes in the network: ')
				G = create_graph(subnw_no)
				mapper = chr(ord('a') + x)
				H = mapping(G,subnw_no,mapper)
				json_data = generate_json(H,subnw_no)
				create_figure(H,subnw_no,path)
				print 'The nodes for Sub-network ' + str(subnw_no) + 'are : ' + str(H.nodes())
				graph_id = insert_mongodb(json_data)
				list_graphs.append(str(graph_id))
			print ('******************************************************************************************************')
			print 'The list of object IDs : ' + str(list_graphs)			
			# for x in range(0,3):
			# client = mongodb_client()
			db = client.mydb
			collection = db.graph_collection
			# temp1 = list_graphs.pop(0)
			# print temp1
			data_graph1 = collection.find_one({'_id': ObjectId(list_graphs[0])})
			# print data_graph1
			G1 = json_graph.node_link_graph(data_graph1, multigraph = False)
			# print G1.nodes()
			# print temp1
			data_graph2 = collection.find_one({'_id': ObjectId(list_graphs[1])})
               		G2 = json_graph.node_link_graph(data_graph2, multigraph = False)
			data_graph3 = collection.find_one({'_id': ObjectId(list_graphs[2])})
             	  	G3 = json_graph.node_link_graph(data_graph3, multigraph = False)
			# client.close()
			'''
			I = nx.compose(G1,G2)
			J = nx.compose(I,G3)
			json_data4 = generate_json(J,4)
			create_figure(J,4)
			# print G1.nodes()
			# print G2.nodes()
			# print G3.nodes()
			print 'The nodes for entire network are : ' + str(J.nodes())
			#path = nx.shortest_path(J, u'a1', u'c0')
			#print path	
			shortestpath(J)
			'''

		elif (i == 2):
			subnw_no_edit = input ('Enter the Sub-network to which a node is to be added: ')
			#startTime1 = time.clock()
			data_graph = retrieve_db(subnw_no_edit)
 	           	subnw_num = data_graph['network']
			mapper = chr(ord('a') + (subnw_no_edit - 1))
			if subnw_num == subnw_no_edit :
				if subnw_no_edit == 1:
					G1 = json_graph.node_link_graph(data_graph, multigraph = False)
					new_node = mapper + str(len(G1) - 1)
                              		print 'The new node that is added is :' + str(new_node)
                               		node_add = unicode(new_node)
					#G1.add_node(new_node)
					#elapsedtime1 = time.clock() - startTime1
                                	edge_add = raw_input ('Enter the node to be attached to the new node: ')
                                	#startTime2 = time.clock()
					chk = check_node(G1, edge_add)
					if (chk == 1):
						startTime = time.time()
						G1.add_node(new_node)
						G1.add_edge(edge_add,new_node)
						print 'An edge is added between the node ' + str(edge_add) + 'and ' + str(new_node)
                                		print 'The nodes of Subnetwork 1 after addition of one node: ' + str(G1.nodes())
						json_data = generate_json(G1,subnw_no_edit)
                                       		remove_mongodb_doc(subnw_no_edit)
						graph_id = insert_mongodb(json_data)
						list_graphs.pop(0)
						list_graphs.insert(0, str(graph_id))
						print list_graphs
						# update_mongodb(new_node,edge_add,subnw_no_edit)
						create_figure(G1,subnw_no_edit,path)
						elapsedtime = time.time() - startTime
						#timeinms = int(round(time.time() * 1000))
						print 'The time required for addition of node:' + str(elapsedtime) 
					else:
						print 'The node to be attached to new node not found in the sub-network'
						check_err = 1
				elif subnw_no_edit == 2:
					# G2 = K.copy()
					G2 = json_graph.node_link_graph(data_graph, multigraph = False)
                                        new_node = mapper + str(len(G2) - 1)
                                        print  'The new node that is added is :' + str(new_node)
					node_add = unicode(new_node)
                                        G2.add_node(new_node)
					#elapsedtime1 = time.clock() - startTime1
                                        edge_add = raw_input ('Enter the node to be attached to the new node: ')
					#startTime2 = time.clock()
                                        chk = check_node(G2, edge_add)
                                        if (chk == 1):
						startTime = time.time()
						G2.add_edge(unicode(edge_add),node_add)
                                        	print 'An edge is added between the node ' + str(edge_add) + 'and ' + str(new_node)
                                        	print 'The nodes of Subnetwork 2 after addition of one node: ' + str(G2.nodes())
						json_data = generate_json(G2,subnw_no_edit)
						remove_mongodb_doc(subnw_no_edit)
                                        	graph_id = insert_mongodb(json_data)
                                        	list_graphs.pop(1)
                                        	list_graphs.insert(1, str(graph_id))
                                        	print list_graphs

						# update_mongodb(new_node,edge_add,subnw_no_edit)
                     				create_figure(G2,subnw_no_edit,path)	
						elapsedtime = time.time() - startTime
						print 'The time required for addition of node:' + str(timeinms)
					else:
						print 'The node to be attached to new node not found in the sub-network'
						check_err = 1
				else:
					#G3 = K.copy()
					G3 = json_graph.node_link_graph(data_graph, multigraph = False)
                                        new_node = mapper + str(len(G3) - 1)
                                        print 'The new node that is added is :' + str(new_node)
                                        node_add = unicode(new_node)
					G3.add_node(new_node)
					#elapsedtime1 = time.clock() - startTime1
                                        edge_add = raw_input ('Enter the node to be attached to the new node: ')
                                        #startTime2 = time.clock()
					chk = check_node(G3, edge_add)
                                        if (chk == 1):
						startTime = time.time()
						G3.add_edge(edge_add,new_node)
                                        	#print G3.nodes()
						print 'An edge is added between the node ' + str(edge_add) + 'and ' + str(new_node)
                                       		print 'The nodes of Subnetwork 3 after addition of one node: ' + str(G3.nodes())
						json_data = generate_json(G3,subnw_no_edit)
						remove_mongodb_doc(subnw_no_edit)
                                        	graph_id = insert_mongodb(json_data)
                                        	list_graphs.pop(2)
                                        	list_graphs.insert(2, str(graph_id))
                                        	print list_graphs
						# update_mongodb(new_node,edge_add,subnw_no_edit)
                                        	create_figure(G3,subnw_no_edit,path)
						elapsedtime = time.time() - startTime
						print 'The time required for addition of node:' + str(timeinms)
					else:
						print 'The node to be attached to new node not found in the sub-network'
						check_err = 1
			else:			
				print 'Graph' + subnw_no_edit + ' not found'
				check_err = 1
						
			#elapsedtime = time.time() - startTime
			#print 'The time required for addition of a node is' + str(elapsedtime)
		else:
			print 'Wrong option selected.'	
			check_err = 1
			break
		
		if check_err == 0 :
		#	if (i == 1):	
			I = nx.compose(G1,G2)
			J = nx.compose(I,G3)
			generate_json(J,4)
			print 'The nodes for entire network are : ' + str(J.nodes())
			path = shortestpath(J)
			create_figure(J,4,path)
			print 'The shortest path is : ' + str(path)
			condition = raw_input ('Do you want to continue?[Y/n] ')
                   	client.close()
			'''
			else:
				I = nx.compose(G1,G2)
                                J = nx.compose(I,G3)
                                generate_json(J,4)
                                print 'The nodes for entire network are : ' + str(J.nodes())
                                path = shortestpath(J)
                                create_figure(J,4,path)
                                print 'The shortest path is : ' + str(path)
                                elapsedtime2 = time.clock() - startTime2
                                totelapsedtime = elapsedtime1 + elapsedtime2
				print 'ElapsedTime 1 =' + str(elapsedtime1) + 'ElapsedTime 2 =' + str(elapsedtime2) + 'and the total time is: ' + str(totelapsedtime)
				print 'The time required for addition of a node is' + str(totelapsedtime)
				condition = raw_input ('Do you want to continue?[Y/n] ')
                                client.close()
			'''	

		else :
			condition = raw_input ('Do you want to continue?[Y/n] ')
			client.close()
	print 'Thank you!' 
