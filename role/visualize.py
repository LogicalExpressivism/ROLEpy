import networkx as nx
from networkx import algorithms
from matplotlib import pyplot as plt
from role import calculus

def graph_prfs(context: calculus.Context):
    g = nx.MultiDiGraph()
    g.add_edges_from((source, target) for (source, targets, _) in context.proofs for target in targets)
    # dig = nx.DiGraph(g)
    # if algorithms.is_directed_acyclic_graph(dig):
    #     print(list(algorithms.topological_sort(nx.line_graph(dig))))
    gstoch = nx.line_graph(g)
    # g = nx.subgraph(g, nx.ancestors(g, 0))
    # @TODO: In progress attempt at fixing nodes that aren't sources or aren't targets of any edge at
    # different sides of the plot.
    # no_ancestors = []
    # no_descendants = []
    # others = []

    # napos = (1,-1)
    # naposdelta = 2. / len(no_ancestors)
    # ndpos = (-1,-1)
    # ndposdelta = 2. / len(no_descendants)
    # for node in g.nodes():
    #     if len(nx.ancestors(g, node)) == 0:
    #         no_ancestors[node] = napos
    #         napos = (napos[0], napos[1] + naposdelta)
    #         continue
    #     if len(nx.descendants(g, node)) == 0:
    #         no_descendants[node] = ndpos
    #         ndpos = (ndpos[0], ndpos[1] + ndposdelta)
    #         continue
    #     others[node] = (0,0)
    pos = nx.spring_layout(gstoch,
        k=1,
        scale=4,
        # pos=[(n, p) for (n, p) in dicts.items() for dicts in [no_ancestors, no_descendants, others]],
        # fixed=[n for n in dicts.keys() for dicts in [no_ancestors, no_descendants]]
        )
    
    plt.figure(figsize=(10,10))
    options = {
        "with_labels": True,
        "edgecolors": "black",
        "edge_color": "black",
        "width": 1,
        "linewidths": 1,
        "node_size": 100,
        "node_color": "pink",
        "alpha": 0.9,
    }
    nx.draw(gstoch, pos=pos, **options,
        # labels={(s, t):(context.get_sq(s), context.get_sq(s)) for (s, t) in gstoch.nodes()}
        )
    nx.draw_networkx_edge_labels(gstoch,pos,
        # edge_labels={(source, target):rule for (source, targets, rule) in context.proofs for target in targets},
        # edge_labels={(edge[0], edge[1]):edge[2] for edge in gstoch.edges},
        font_color='red')
    plt.axis('off')
    plt.show()
        
