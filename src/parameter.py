class Parameters:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._window_type = 'depth'
            cls._instance._window_size = 3
            cls._instance._context_structure = 'multiset'
            cls._instance._include_semantic = True
            cls._instance._clustering_algo = 'agglomerative'
            cls._instance._probability_threshold = 0
            cls._instance._propagation_threshold = 1.0
            cls._instance._postprocess_strategy = 'context'
            cls._instance._optimal_number_of_concepts = 5
        return cls._instance


    @property
    def window_type(self):
        return self._window_type

    @window_type.setter
    def window_type(self, value):
        possible_values = ['depth', 'time']
        if value not in possible_values:
            raise ValueError(f"Invalid value '{value}' for window_type")
        self._window_type = value

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        self._window_size = value

    @property
    def context_structure(self):
        return self._context_structure

    @context_structure.setter
    def context_structure(self, value):
        possible_values = ['set', 'multiset']
        if value not in possible_values:
            raise ValueError(f"Invalid value '{value}' for context_structure")
        self._context_structure = value

    @property
    def probability_threshold(self):
        return self._probability_threshold

    @probability_threshold.setter
    def probability_threshold(self, value):
        if not 0 <= value <= 1:
            raise ValueError("Probability threshold must be between 0 and 1")
        self._probability_threshold = value

    @property
    def include_semantic(self):
        return self._include_semantic

    @include_semantic.setter
    def include_semantic(self, value):
        if not isinstance(value, bool):
            raise ValueError("Include semantic must be a boolean value")
        self._include_semantic = value

    @property
    def clustering_algo(self):
        return self._clustering_algo

    @clustering_algo.setter
    def clustering_algo(self, value):
        possible_values = ['hdbscan', 'dbscan', 'spectral', 'agglomerative', 'kmedoids']
        if value not in possible_values:
            raise ValueError(f"Invalid value '{value}' for clustering_algo")
        self._clustering_algo = value

    @property
    def propagation_threshold(self):
        return self._propagation_threshold

    @propagation_threshold.setter
    def propagation_threshold(self, value):
        if not 0 <= value <= 1:
            raise ValueError("Propagation threshold must be between 0 and 1")
        self._propagation_threshold = value


    @property
    def postprocess_strategy(self):
        return self._postprocess_strategy

    @postprocess_strategy.setter
    def postprocess_strategy(self, value):
        possible_values = ['context', 'weightedsurr', 'random', 'none']
        if value not in possible_values:
            raise ValueError(f"Invalid value '{value}' for postprocess_strategy")
        self._postprocess_strategy = value

    @property
    def optimal_number_of_concepts(self):
        return self._optimal_number_of_concepts

    @optimal_number_of_concepts.setter
    def optimal_number_of_concepts(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Optimal number of concepts must be a non-negative integer")
        self._optimal_number_of_concepts = value

    def __str__(self):
        attributes = vars(self)
        attributes_str = "\n".join([f"{attr}: {getattr(self, attr)}" for attr in attributes])
        return attributes_str

    def to_dict(self):
        return {
            "window_type": self._window_type,
            "window_size": self._window_size,
            "context_structure": self._context_structure,
            "include_semantic": self._include_semantic,
            "clustering_algo": self._clustering_algo,
            "probability_threshold": self._probability_threshold,
            "propagation_threshold": self._propagation_threshold,
            "optimal_number_of_concepts": self._optimal_number_of_concepts
        }
