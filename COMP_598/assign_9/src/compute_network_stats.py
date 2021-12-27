from networkx.algorithms.centrality.load import _node_betweenness
import pandas as pd
import networkx as nx
import numpy as np
import argparse
import json
#-i
#-o
parser = argparse.ArgumentParser()
parser.add_argument('-i','--interaction_json',help='interactions')
parser.add_argument('-o','--output_file', help='stats output')
args = parser.parse_args()

input = args.interaction_json
output = args.output_file

def main():
    with open(input,'r') as f:
        interactions = json.load(f)
    G = nx.Graph()
    i=0
    for node in interactions:
        for edge in interactions[node]:
            
            G.add_edge(node,edge,weight=interactions[node][edge])
    #G = nx.DiGraph(interactions)
    #G.to_undirected
    output_json = {}

    #get degrees of nodes
    node_degrees = {}
    for v in G.nodes():
        node_degrees[v] = G.degree(v)
    
    #sort the nodes and their degrees by largest degrees
    deg_list = list(node_degrees.items())
    deg_list.sort(key=lambda x: -x[1])
    deg = [deg_list[0][0],deg_list[1][0],deg_list[2][0]]
    output_json.update({'most_connected_by_num':deg})

    #sum of weights of the edges
    for v in G.nodes():
        node_degrees[v] = G.degree(v,weight='weight')
    node_list = list(node_degrees.items())
    weight_list = sorted(node_list,key=lambda x: x[1],reverse=True)[:3]
    w = [weight_list[0][0],weight_list[1][0],weight_list[2][0]]
    output_json.update({'most_connected_by_weight':w})

    #highest betweenes
    node_betweenness = nx.betweenness_centrality(G)
    between_list = list(node_betweenness.items())
    between_list.sort(key=lambda x: -x[1])
    deg = [ between_list[0][0],between_list[1][0],between_list[2][0] ]
    output_json.update({'most_central_by_betweenness':deg})

    with open(output,'w') as f:
        json.dump(output_json,f,indent=4)
    

if __name__ == '__main__':
    main()
