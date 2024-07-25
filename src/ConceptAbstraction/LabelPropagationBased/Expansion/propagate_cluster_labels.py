from networkx import DiGraph
from sklearn.semi_supervised import LabelPropagation
from heapo.parameter import Parameters
import numpy as np
import networkx as nx
from heapo.objects.po_log import POLog


param = Parameters()


def propagate_labels_with_weights(graph: DiGraph, label_name: str = 'cluster_id'):

    max_neighbor_cnt = max([len(graph.in_edges(node))+len(graph.out_edges(node)) for node in graph])

    # Extract labeled nodes and their corresponding labels
    labels = [graph.nodes[node][label_name] for node in graph.nodes]

    # Create adjacency matrix with weights
    adjacency_matrix = nx.adjacency_matrix(graph, weight='weight').toarray()

    # Compute graph Laplacian matrix
    laplacian_matrix = np.diag(np.sum(adjacency_matrix, axis=1)) - adjacency_matrix

    # Initialize LabelPropagation model
    try:
        lp_model = LabelPropagation(kernel='knn', n_neighbors=max_neighbor_cnt)
    except:
        lp_model = LabelPropagation(kernel='knn')

    lp_model.fit(laplacian_matrix, labels)

    # Predict labels for all nodes
    predicted_labels = lp_model.transduction_

    # Update node labels in the graph based on the threshold
    changed_labels = 0
    for i, node in enumerate(graph.nodes):
        if np.max(lp_model.label_distributions_[i]) >= param.propagation_threshold:
            if graph.nodes[node][label_name] != predicted_labels[i]:
                changed_labels += 1
            graph.nodes[node][label_name] = predicted_labels[i]

    return lp_model, changed_labels, predicted_labels, labels


def apply(log: POLog):
    for po_case in log:
        if len(po_case) > 1 and not all(
                value == -1 for value in {po_case.nodes[node]['cluster_id'] for node in po_case.nodes}):
            lp_model, changed_labels, predicted_labels, original_labels = propagate_labels_with_weights(po_case,
                                                                                                        'cluster_id')
