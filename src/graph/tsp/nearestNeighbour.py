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
        for _ in range(self.graph.vertex_count - 1):
            # choose the smallest edge in the list of edges where the end vertex isn't present yet
            current_edge = min([_ for _ in current_vertex.edges if _.end not in self.round_trip.vertexes])
            self.round_trip.add_existing_edge(current_edge)
            current_vertex = current_edge.end
        # get the edge back to the start vertex
        final_edge = self.graph.get_edge(start_v=current_vertex.value, end_v=start_vertex.value)
        # add the last edge back to the start to close the round trip
        self.round_trip.add_existing_edge(final_edge)
        return self.round_trip
