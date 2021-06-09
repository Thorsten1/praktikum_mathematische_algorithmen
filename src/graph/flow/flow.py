# flow class
from graph import Graph, Edge, Vertex


class FlowEdge(Edge):
    def __init__(self, start: Vertex, end: Vertex, capacity: int, flow=0, weight=0):
        super(FlowEdge, self).__init__(start, end, weight)
        self.flow = flow
        self.capacity = capacity


class Flow(Graph):
    def __init__(self, vertex_count=0, weighted=False):
        super(Flow, self).__init__(vertex_count=vertex_count, directed=True, weighted=weighted)

    def add_existing_edge(self, edge: FlowEdge):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        This will not take the old vertexes but generate new ones to strip them from theire edges
        :param edge: The edge that shall be added
        :return: void
        """
        # Generate a new edge and new vertexes so they aren't related to the old graph
        if not self.vertexes.get(edge.start.value):
            self.vertexes[edge.start.value] = Vertex(edge.start.value)
        if not self.vertexes.get(edge.end.value):
            self.vertexes[edge.end.value] = Vertex(edge.end.value)
        self.add_edge(edge.start.value, edge.end.value, edge.weight, edge.flow, edge.capacity)

    def add_edge(self, start: int, end: int, capacity: int, flow=0, weight=0):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        :param start:
        :param end:
        :param weight:
        :param capacity:
        :param flow
        :return: void
        """
        start_v = self.vertexes.get(start)
        end_v = self.vertexes.get(end)

        # Create a new edge object and add it to the internal list of edges.
        # Although it is not required for operating on graphs, it will be used
        # for optimized performance and avoid iterating over all vertexes.
        edge = FlowEdge(start_v, end_v, weight=weight, capacity=capacity, flow=flow)
        self.edges[start_v][end_v] = edge

        # Add the edge to its start vertex
        start_v.add_edge(edge)
