from graph.graph import timeit, Graph
from graph.flow.flow import Flow

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
        while True:
            # Step 2: Get residual graph for current flow graph.
            g_f = self.__residual_graph(self.graph)

            break

        return 0

    @staticmethod
    def __residual_graph(graph: Flow):
        g_f = Flow(vertex_count=graph.vertex_count)
        for v in graph.vertexes.values():
            for e in v.edges:
                # residual capacity
                if e.flow > 0:
                    g_f.add_edge(e.end, e.start, e.flow)

                # remaining capacity
                u = e.capacity - e.flow
                if u > 0:
                    g_f.add_edge(e.start, e.end, u)

        return g_f
