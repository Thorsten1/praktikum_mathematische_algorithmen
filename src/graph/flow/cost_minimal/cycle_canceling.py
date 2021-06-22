from .abstractFlowCostmin import AbstractCostminFlow
from ..flow import residual_graph, Flow, BalanceVertex, FlowEdge
from ...graph import timeit
from ..max.edmondsKarp import EdmondsKarp
from ...shortest_path.mooreBellmanFord import MooreBellmanFord

from typing import Optional


class CycleCanceling(AbstractCostminFlow):
    """
    """

    def __call__(self):
        """
        """
        return self._cycle_canceling()

    @staticmethod
    def __bFlow(flow: Flow) -> Optional[Flow]:
        """
        Generate a b-Flow.


        :param flow: The flow to get the b-Flow from.

        :returns: A b-Flow or :py:class:`None`, if no b-Flow exists.
        """
        # Generate a super source and target to accumulate multiple ones into
        # just a single one.
        s = flow.add_vertex(flow.vertex_count)
        for sv in filter(lambda v: v.balance > 0, list(flow.vertexes.values())):
            flow.add_existing_edge(FlowEdge(s, sv, sv.balance))
        t = flow.add_vertex(flow.vertex_count)
        for tv in filter(lambda v: v.balance < 0, list(flow.vertexes.values())):
            flow.add_existing_edge(FlowEdge(tv, t, tv.balance * -1))

        # Generate a maximum flow from super source to super target. If all
        # edges to / from source and target use their full capacity, its a
        # b-Flow and it can be returned, except for the super vertexes.
        maxFlow = EdmondsKarp(flow)(s, t)
        if all(map(lambda e: e.capacity == e.flow,
                   filter(lambda e: e.start == s or e.end == t,
                          flow._flatten_edges()))):
            maxFlow.remove_vertex(maxFlow.vertex_count - 1)
            maxFlow.remove_vertex(maxFlow.vertex_count - 1)
            return maxFlow

    def __negativeCycle(self, residual: Flow, start: int = 0) -> Optional[Flow]:
        """
        Find a negative cost cycle in `residual` graph.


        :param residual: The residual graph to be searched.
        :param start: At which node to start the search.
        """
        (_, predecessor, hist) = MooreBellmanFord(residual)(start)
        if not hist:
            return

        # If a negative cycle has been found, search for the first vertex to be
        # in this cycle.
        v = hist[len(hist) - 1 - residual.vertex_count]
        visited = [v]
        while True:
            v = predecessor[v]
            if v in visited:
                break
            visited.append(v)

        # Starting from the vertex found above, a complete iteration of edges in
        # this cycle will be yielded to be processed by other methods of this
        # class.
        s = v
        while True:
            p = predecessor[v]
            yield residual.edges[p][v]
            v = p
            if v == s:
                break

    @timeit
    def _cycle_canceling(self) -> Optional[Flow]:
        """
        :param int start: The start of our flow
        :param int target: The end of our flow

        :return The maximum flow
        """
        # Step 1: Generate initial flow
        flow = self.__bFlow(self.graph)
        if not flow:
            return

        while True:
            # Execute steps 2 and 3 combined.
            #
            # Step 2: Generate residual graph
            #
            # Step 3: Get a cycle with negative cost inside the residual graph.
            #         If none can be found, the loop will be exited, as there
            #         are no further optimizations possible.
            c = list(self.__negativeCycle(residual_graph(flow)))
            if not c:
                break

            # Step 4: Update flow along cycle c with its minimum capacity.
            ymin = min(map(lambda e: e.capacity, c))
            for pe in c:
                if not pe.residual:
                    flow.edges[pe.start][pe.end].flow += ymin
                else:
                    flow.edges[pe.end][pe.start].flow -= ymin

        self.cost = sum(map(lambda e: e.weight * e.flow, flow._flatten_edges()))
        return flow
