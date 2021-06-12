import abc

from ..flow import Flow, BalanceVertex


class AbstractCostminFlow(abc.ABC):
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
                self.graph.vertexes[i] = BalanceVertex(value=i, balance=input_file.readline())
            for knot in input_file:
                s, e, cost, cap = knot.split("\t")
                self.graph.add_edge(int(s), int(e), weight=float(cost.replace('\n', '')), capacity=float(cap))

    @abc.abstractmethod
    def __call__(self):
        """
        """
        pass
