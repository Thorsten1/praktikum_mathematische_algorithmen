from .abstractFlowCostmin import AbstractCostminFlow
from ..flow import Flow, BalanceVertex, FlowEdge
from ...graph import timeit
from ..max.edmondsKarp import EdmondsKarp

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
