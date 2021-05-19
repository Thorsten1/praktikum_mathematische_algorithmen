import abc

from graph.graph import Graph, Vertex
from graph.graph import timeit


class TSP(abc.ABC):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.round_trip = None

    @timeit
    def import_from_file(self, filepath):
        """
        Import the given file as mst

        :param filepath: the path to the graph file
        :return: void
        """
        with open(filepath, "r") as input_file:
            self.graph = Graph(weighted=True, vertex_count=int(input_file.readline()))
            self.round_trip = Graph(weighted=True, vertex_count=self.graph.vertex_count)
            for i in range(self.graph.vertex_count):
                self.graph.vertexes[i] = Vertex(value=i)
            for knot in input_file:
                s, e, w = knot.split("\t")
                self.graph.add_edge(int(s), int(e), float(w.replace('\n', '')))

    @abc.abstractmethod
    def __call__(self):
        """
        """
        pass
