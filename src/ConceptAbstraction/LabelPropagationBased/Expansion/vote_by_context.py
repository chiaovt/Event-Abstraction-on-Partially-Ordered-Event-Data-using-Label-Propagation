from typing import Dict, List
from collections import defaultdict
import statistics
from heapo.objects.po_log import POLog
import random


def is_dominating_smaller(value, lst, dominating_threshold = 0.5):
    # Count the number of times the value is smaller than others
    count_smaller = sum(1 for other_value in lst if other_value > value)
    # Calculate the ratio of smaller comparisons
    ratio_smaller = count_smaller / (len(lst) - 1)  # Exclude the value itself
    # Check if the ratio is sufficiently high to consider the value as dominating smaller
    return ratio_smaller > dominating_threshold


def collect_major_similar_clusters(clusterid2dist: Dict[int, float]) -> List[int]:
    potential_cluster_ids = []
    for cluster_id, to_cluster_distance in clusterid2dist.items():
        if len(clusterid2dist.values()) > 1 and is_dominating_smaller(to_cluster_distance, list(clusterid2dist.values()), 0.2):
            potential_cluster_ids.append(cluster_id)
    return potential_cluster_ids


def get_dominating_cluster_id(clusterid2dist: Dict[int, float]) -> int or None:
    for cluster_id, to_cluster_distance in clusterid2dist.items():
        if len(clusterid2dist.values()) > 1 and is_dominating_smaller(to_cluster_distance, list(clusterid2dist.values())):
            return cluster_id
    return None


def collect_instance_per_cluster_id(log: POLog) -> Dict[int, List[int]]:
    clusterid_to_instanceidarray = defaultdict(list)
    for po_case in log:
        for instance_id in po_case.instances:
            if po_case.instances[instance_id]['cluster_id'] != -1:
                clusterid_to_instanceidarray[po_case.instances[instance_id]['cluster_id']].append(instance_id)
    return clusterid_to_instanceidarray

def compute_instance_to_cluster_distance(instance_id: int, instances_in_cluster: List[int], iid_dist_matrix) -> float:
    distances = [iid_dist_matrix[instance_id-1, inst_in_cluster - 1] for inst_in_cluster in instances_in_cluster]
    return statistics.median(distances)


def apply(log: POLog, iid_dist_matrix) -> None:
    clusterid_to_instanceidarray = collect_instance_per_cluster_id(log)

    for po_case in log:
        unlabeled_instances = [instance_id for instance_id in po_case.instances if po_case.instances[instance_id]['cluster_id'] == -1]
        for unable_inst in unlabeled_instances:

            clusterid2dist = {cluster_id: compute_instance_to_cluster_distance(unable_inst, instances, iid_dist_matrix)
                              for cluster_id, instances in clusterid_to_instanceidarray.items()}

            min_dist = round(min(clusterid2dist.values()), 4)
            closest_cluster_ids = {cluster_id for cluster_id, dist in clusterid2dist.items() if round(dist, 4) == min_dist}
            po_case.instances[unable_inst]['cluster_id'] = random.choice(list(closest_cluster_ids))

