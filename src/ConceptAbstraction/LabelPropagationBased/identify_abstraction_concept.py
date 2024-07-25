from heapo.ConceptAbstraction.LabelPropagationBased.Initialization import initialize
from heapo.ConceptAbstraction.LabelPropagationBased.Expansion import expand
from heapo.objects.po_log import POLog


def apply(log: POLog) -> None:
    instance_distances = initialize.apply(log) # clustering algorithm or assigned
    expand.apply(log, instance_distances) # 3 strategies
