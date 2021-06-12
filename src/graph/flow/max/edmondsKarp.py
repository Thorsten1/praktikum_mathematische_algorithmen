from graph.graph import timeit

from .abstractFlowMax import AbstractMaxFlow
from ..flow import residual_graph


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
            g_f = residual_graph(self.graph)
            # Step 3: Get shortest path (number of edges) from start to target.
            #         If no path could be found, the algorithm hits its end and
            #         finishes.
            p = self.graph.bfs(g_f.vertexes.get(target),
                               g_f.vertexes.get(start))
            if not p:
                break

            # Step 4: Update flow along path p with its minimum capacity.
            ymin = min(map(lambda e: e.capacity, p))
            for pe in p:
                if not pe.residual:
                    self.graph.edges[pe.start][pe.end].flow += ymin
                else:
                    self.graph.edges[pe.end][pe.start].flow -= ymin

        self.flow = sum(map(lambda e: e.flow, self.graph.vertexes[start].edges))
        return self.graph
