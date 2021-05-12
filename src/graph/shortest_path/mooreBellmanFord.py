from graph.graph import timeit
from graph.shortest_path.abstractShortestPath import ShortestPath


class MooreBellmanFord(ShortestPath):
    def __init__(self):
        super().__init__()
        self.distance = [float('Inf') for _ in range(self.graph.vertex_count)]
        self.predecessors = [None for _ in range(self.graph.vertex_count)]

    def __call__(self):
        return self._moore_bellman_ford()

    @timeit
    def _moore_bellman_ford(self):
        pass
