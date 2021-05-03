from graph import Graph, timeit, TSP, Kruskal


class DoubleTree(TSP):
    def __init__(self):
        super().__init__()

    def __call__(self):
        return self._double_tree()

    @timeit
    def _double_tree(self) -> Graph:
        """
        determine a minimal round trip using double_tree
        :return: The Graph for the round trip
        """
        # get an mst from the graph using Kruskal
        kruskal = Kruskal(self.graph)
        mst = kruskal.get_mst()
        # get the trip list using DFS
        trip_vertex_list = mst.dfs()
        # iterate through the list until you reach the last item
        for i in range(len(trip_vertex_list) - 1):
            # always add the edge to the next vertex
            current_edge = next(_ for _ in self.graph.vertexes.get(trip_vertex_list[i]).edges if _ == f"{trip_vertex_list[i]}:{trip_vertex_list[i + 1]}")
            self.round_trip.add_existing_edge(current_edge)
        # Add the Last edge back to the start
        current_edge = next(_ for _ in self.graph.vertexes.get(trip_vertex_list[-1]).edges if _ == f"{trip_vertex_list[-1]}:{trip_vertex_list[0]}")
        self.round_trip.add_existing_edge(current_edge)
        return self.round_trip
