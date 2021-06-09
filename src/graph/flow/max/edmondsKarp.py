from graph.graph import timeit, Graph

from .abstractFlowMax import AbstractMaxFlow


class EdmondsKarp(AbstractMaxFlow):
    """
    """

    def __call__(self, start, target):
        """
        """
        return self._edmondsKarp(start, target)

    @timeit
    def _edmondsKarp(self, start, target):
        """
        :param int start: The start of our flow
        :param int target: The end of our flow
        :return The maximum flow
        """
        maxFlow = 0
        flows = [0 for _ in range(len(self.graph.edges))]
        g_f = self.__residual_graph()

        return maxFlow

    def __residual_graph(self) -> Graph:
        # generate the residual graph with residualcapcitys as weight
        g_f = Graph(vertex_count=self.graph.vertex_count, directed=True, weighted=True)
        for v in self.graph.vertexes:
            for e in v.edges:
                g_f.add_existing_edge(edge=e)
                g_f.add_edge(e.end, e.start, 0)
        return g_f
