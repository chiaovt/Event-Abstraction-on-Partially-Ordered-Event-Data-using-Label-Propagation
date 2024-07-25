import numpy as np


def normalize_by_min_max(values):
    max_value = np.max(values)
    min_value = np.min(values)
    noramlized_values = (values - min_value) / (max_value - min_value)
    return noramlized_values