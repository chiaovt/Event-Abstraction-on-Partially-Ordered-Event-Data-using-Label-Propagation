from heapo.ConceptAbstraction.LabelPropagationBased.Expansion import propagate_cluster_labels, vote_by_context, vote_by_weighted_surrounding, vote_randomly
from heapo.objects.po_log import POLog
from heapo.parameter import Parameters
from heapo.ConceptAbstraction.LabelPropagationBased.Initialization.Clustering.Utility import util as clustering_util


param = Parameters()

def annotate_distance_as_weight(log, iid_dist_matrix):

    similarity_matrix = clustering_util.convert_to_similarity_matrix(iid_dist_matrix)
    for po_case in log:
        for edge in po_case.edges():
            instance1_id = po_case.get_iid_by_node_id(edge[0])
            instance2_id = po_case.get_iid_by_node_id(edge[1])
            po_case[edge[0]][edge[1]]['weight'] = similarity_matrix[instance1_id-1, instance2_id-1]


def apply(log: POLog, iid_dist_matrix) -> None:

    annotate_distance_as_weight(log, iid_dist_matrix)

    propagate_cluster_labels.apply(log)

    # post_processing
    if param.postprocess_strategy == 'context':
        vote_by_context.apply(log, iid_dist_matrix)
    elif param.postprocess_strategy == 'weighted':
        vote_by_weighted_surrounding.apply(log)
    elif param.postprocess_strategy == 'random':
        vote_randomly.apply(log)
