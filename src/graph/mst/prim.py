import heapq

from graph.graph import Edge, timeit
from graph.mst.abstractMst import MST


class Prim(MST):
    def __init__(self):
        super().__init__()

    def __call__(self):
        return self._prim()

    @timeit
    def _prim(self) -> int:
        """
        Implements the Prim Algorithm for the MST
        :return: Returns the cost of the MST
        """
        # a set to mark all visited vertexes
        visited_vertexes = set()
        # the overall weight cost of the mst
        mst_cost = 0
        # priority queue to always add the smallest edge to the mst
        priority_queue = []
        # first element is set beforehand
        start_v = self.graph.vertexes.get(0)
        # transform start Vertex into Edge
        current_edge: Edge = Edge(start_v, start_v, 0)
        # python do-while implementation so first execution works with empty priority queue
        while True:
            if current_edge.end.value not in visited_vertexes:
                visited_vertexes.add(current_edge.end.value)
                mst_cost += current_edge.weight
                for edge in current_edge.end.edges:
                    if edge.end.value not in visited_vertexes:
                        heapq.heappush(priority_queue, edge)
            if priority_queue and len(visited_vertexes) < len(self.graph.vertexes):
                current_edge = heapq.heappop(priority_queue)
            else:
                break
        return mst_cost
