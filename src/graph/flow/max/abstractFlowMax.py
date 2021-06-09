import abc

from graph import Graph, Vertex

from graph.flow.flow import Flow, FlowEdge


class AbstractMaxFlow(abc.ABC):
    def __init__(self, graph=None):
        super().__init__()
        self.graph = graph or Flow()

    def import_from_file(self, filepath):
        """
        Import the given file as weighted graph

        :param filepath: the path to the graph file
        :return: void
        """
        with open(filepath, "r") as input_file:
            self.graph = Flow(vertex_count=int(input_file.readline()))
            for i in range(self.graph.vertex_count):
                self.graph.vertexes[i] = Vertex(value=i)
            for knot in input_file:
                s, e, c = knot.split("\t")
                self.graph.add_edge(int(s), int(e), float(c.replace('\n', '')))

    @abc.abstractmethod
    def __call__(self, start, target):
        """
        """
        pass
