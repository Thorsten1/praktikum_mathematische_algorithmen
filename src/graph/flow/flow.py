# flow class
from graph import Graph, Edge, Vertex


class BalanceVertex(Vertex):
    def __init__(self, value: int, balance=0, edges=None):
        super(BalanceVertex, self).__init__(value=value, edges=edges)
        self.balance = balance


class FlowEdge(Edge):
    def __init__(self, start: Vertex, end: Vertex, capacity: int, flow=0, weight=0, residual=False):
        super(FlowEdge, self).__init__(start, end, weight)
        self.flow = flow
        self.capacity = capacity
        self.residual = residual

    def __str__(self):
        return f"{self.start} -> {self.end} ({self.flow} / {self.capacity})"


class Flow(Graph):
    def __init__(self, vertex_count=0, weighted=False):
        super(Flow, self).__init__(vertex_count=vertex_count,
                                   directed=True, weighted=weighted)
        self.vertexes = {i: BalanceVertex(value=i) for i in range(self.vertex_count)}

    def add_existing_edge(self, edge: FlowEdge):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        This will not take the old vertexes but generate new ones to strip them from theire edges
        :param edge: The edge that shall be added
        :return: void
        """
        # Generate a new edge and new vertexes so they aren't related to the old graph
        if not self.vertexes.get(edge.start.value):
            self.vertexes[edge.start.value] = BalanceVertex(edge.start.value)
        if not self.vertexes.get(edge.end.value):
            self.vertexes[edge.end.value] = BalanceVertex(edge.end.value)
        self.add_edge(edge.start.value, edge.end.value,
                      edge.weight, edge.flow, edge.capacity)

    def add_edge(self, start: int, end: int, capacity: float, flow=0, weight=0, residual=False):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        :param start:
        :param end:
        :param weight:
        :param capacity:
        :param flow
        :param residual:
        :return: void
        """
        start_v = self.vertexes.get(start)
        end_v = self.vertexes.get(end)

        # Create a new edge object and add it to the internal list of edges.
        # Although it is not required for operating on graphs, it will be used
        # for optimized performance and avoid iterating over all vertexes.
        edge = FlowEdge(start_v, end_v, weight=weight,
                        capacity=capacity, flow=flow, residual=residual)
        self.edges[start_v][end_v] = edge

        # Add the edge to its start vertex
        start_v.add_edge(edge)

    def _flatten_edges(self):
        for s in self.edges:
            for e in self.edges[s]:
                yield self.edges[s][e]

    def __str__(self):
        flow = list(filter(lambda e: e.flow > 0, self._flatten_edges()))
        return f"{flow}"


def residual_graph(graph: Flow):
    g_f = Flow(vertex_count=graph.vertex_count)
    for v in graph.vertexes.values():
        for e in v.edges:
            # residual capacity
            if e.flow > 0:
                g_f.add_edge(e.end, e.start, capacity=e.flow, weight=-e.weight, residual=True)
            # remaining capacity
            u = e.capacity - e.flow
            if u > 0:
                g_f.add_edge(e.start, e.end, capacity=u, weight=e.weight)

    return g_f
