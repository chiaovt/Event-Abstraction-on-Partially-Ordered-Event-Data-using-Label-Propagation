from typing import Dict, Set, Any, List
from collections import defaultdict
from heapo.objects.po_log import POLog
from heapo.ConceptAbstraction.LabelPropagationBased import name_abstraction_concept
import json
from Experiment.Setup.setup import Setup
from Experiment.DataIO.util import name_file_based_on_last_setting


setup = Setup()


def extract_cluster_id_to_elements_relation(log: POLog) -> Dict[int, Set[str]]:
    cluster2elements_dicto = defaultdict(set)
    for po_case in log:
        for node in po_case.nodes:
            cluster2elements_dicto[po_case.instances[node]['cluster_id']].add(po_case.nodes[node]['name'])
    return cluster2elements_dicto

def append_potential_abstraction_concept_names(log: POLog, clusterid2abstractionconceptname_dicto: Dict[int, str]) -> None:
    for process_case in log:
        for node in process_case.nodes():
            if process_case.nodes[node]['cluster_id'] != -1:
                process_case.nodes[node]['abstracted_name'] = clusterid2abstractionconceptname_dicto[process_case.nodes[node]['cluster_id']]
            else:
                process_case.nodes[node]['abstracted_name'] = process_case.nodes[node]['name']


def merge_cluster_based_on_labels(cluster2elements_dicto):
    elements2clusterids_dicto = defaultdict(list)
    for cluster_id, elements in cluster2elements_dicto.items():
        elements2clusterids_dicto['@@'.join(sorted(elements))].append(cluster_id)
    return elements2clusterids_dicto


def name_abstractionconcept_by_elements(elements_collection: List[List[str]]):
    elements_str_to_name = dict()
    for elements in elements_collection:
        title = name_abstraction_concept.name_title(elements)
        elements_str_to_name['@@'.join(sorted(elements))] = title
    return elements_str_to_name


def append_abstractionconceptname(log: POLog, clusterid2abstractionconceptname_dicto):

    for po_case in log:
        for instance in po_case.instances:
            if po_case.instances[instance]['cluster_id'] != -1:
                po_case.instances[instance]['abstracted_name'] = clusterid2abstractionconceptname_dicto[po_case.instances[instance]['cluster_id']]
            else:
                po_case.instances[instance]['abstracted_name'] = po_case.instances[instance]['name']


def extract_complete_abstraction_details(log: POLog):
    details = dict()
    for po_case in log:
        for instance in po_case.instances:
            if po_case.instances[instance]['abstracted_name'] not in details:
                details[po_case.instances[instance]['abstracted_name']] = {'elements': [], 'cluster_ids': []}
            details[po_case.instances[instance]['abstracted_name']]['elements'].append(po_case.instances[instance]['name'])
            details[po_case.instances[instance]['abstracted_name']]['cluster_ids'].append(po_case.instances[instance]['cluster_id'])
    return details


def write_abstraction_classes(elements2clusterids_dicto):
    clusterid2names = {'+'.join([str(cluster_id) for cluster_id in cluster_ids]) : elemstr.split('@@') for elemstr, cluster_ids in elements2clusterids_dicto.items()}
    filename = name_file_based_on_last_setting('clusterid2abstraction', 'json', 'postprocess_strategy')
    with open(setup.curr_var_com_dir+filename, 'w') as f:
        json.dump(clusterid2names, f)


def read_abstraction_classes():
    filename = name_file_based_on_last_setting('abstractionnaming', 'json', 'postprocess_strategy')
    with open(setup.curr_var_com_dir+filename) as f:
        data = json.load(f)
        return {int(cluster_id): dicto['name'] for cluster_id, dicto in data.items()}


def apply(log: POLog) -> Dict[str, Dict[str, List[Any]]]:
    cluster2elements_dicto = extract_cluster_id_to_elements_relation(log)
    elements2clusterids_dicto = merge_cluster_based_on_labels(cluster2elements_dicto)
    write_abstraction_classes(elements2clusterids_dicto)
    clusterid2abstractionconceptname_dicto = read_abstraction_classes()

    append_abstractionconceptname(log, clusterid2abstractionconceptname_dicto)

    abstraction_details = extract_complete_abstraction_details(log)

    return abstraction_details
