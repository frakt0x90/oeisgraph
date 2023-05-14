import networkx
from networkx.drawing.nx_pydot import write_dot
from tinydb import TinyDB
from typing import List, Dict
from oeisutil import int_to_oeis_seq
from plotnine import ggplot, aes, geom_density


def get_node_dict(db_data: List[Dict[str, Dict[str, List[str]]]]) -> Dict[str, List[str]]:
    graph_data = {}
    for entry in db_data:
        seq_num = tuple(entry.keys())[0]
        links = entry[seq_num]['links']
        graph_data[seq_num] = links
    return graph_data

db = TinyDB('sequences.json')
data = db.all()
graph_data = get_node_dict(data)

G = networkx.Graph(graph_data)
subgraph_nodes = map(int_to_oeis_seq, range(1,10001))
subgraph = networkx.Graph(G.subgraph(subgraph_nodes))

low_deg_nodes = [node for node, degree in dict(G.degree()).items() if degree < 3]
low_deg_nodes_subg = [node for node, degree in dict(subgraph.degree()).items() if degree < 3]
degrees = [degree for node, degree in dict(G.degree()).items()]
G.remove_nodes_from(low_deg_nodes)
#subgraph.remove_nodes_from(low_deg_nodes_subg)
networkx.write_gexf(G, 'high_deg_subgraph.gexf')
networkx.write_gexf(subgraph, 'high_deg_subgraph10k.gexf')