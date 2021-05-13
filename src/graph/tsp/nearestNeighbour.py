from graph.graph import Graph, timeit
from graph.tsp.abstractTSP import TSP


class NearestNeighbour(TSP):
    def __init__(self):
        super().__init__()

    def __call__(self):
        return self._nearest_neighbour()

    @timeit
    def _nearest_neighbour(self) -> Graph:
        """
        determine a minimal round trip using nearest_neighbour
        :return: The Graph for the round trip
        """
        # choose the 0 vertex as start vertex
        start_vertex = self.graph.vertexes[0]
        current_vertex = start_vertex
        # proceed until all vertexes are present within the round trip graph
        while self.round_trip.vertex_count < self.graph.vertex_count:
            # choose the smallest edge in the list of edges where the end vertex isn't present yet
            current_edge = next((_ for _ in sorted(current_vertex.edges) if _.end not in self.round_trip.vertexes), None)
            if current_edge is None:
                break
            self.round_trip.add_existing_edge(current_edge)
            current_vertex = current_edge.end
        # get the edge back to the start vertex
        final_edge = next(_ for _ in current_vertex.edges if _ == f"{current_vertex}:{start_vertex}")
        # add the last edge back to the start to close the round trip
        self.round_trip.add_existing_edge(final_edge)
        return self.round_trip
