from heapo.ConceptAbstraction.LabelPropagationBased import identify_abstraction_concept
from heapo.ConceptAbstraction import extract_abstraction_concept
from heapo.objects.po_log import POLog
from typing import Dict, Any, List


def apply(log: POLog) -> List[Dict[str, Any]]:
    identify_abstraction_concept.apply(log)
    return extract_abstraction_concept.apply(log)

