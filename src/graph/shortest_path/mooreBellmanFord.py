from graph.graph import timeit
from graph.shortest_path.abstractShortestPath import ShortestPath


class MooreBellmanFord(ShortestPath):
    def __init__(self):
        super().__init__()

    def __call__(self, start_vertex: int):
        return self._moore_bellman_ford(start_vertex)

    @timeit
    def _moore_bellman_ford(self, start_vertex: int) -> tuple[list, list]:
        """
        Execute the Moore Bellman Ford Algorithm from the provided start vertex
        :param start_vertex: The Vertex from where to start
        :return: Two lists of distances and predecessors
        """
        # initialize the distances with infinity and their predecessors with None because they aren't known yet
        self.distance = [float('Inf') for _ in range(self.graph.vertex_count)]
        self.predecessors = [None for _ in range(self.graph.vertex_count)]
        # The distance to our start point is 0
        self.distance[start_vertex] = 0
        # Initialize a break condition if nothing has changed within an iteration
        found_better_distance = [False for _ in range(self.graph.vertex_count)]
        # Repeat n-1 times
        for _ in range(self.graph.vertex_count - 1):
            for start in self.graph.vertexes:
                for edge in self.graph.edges[start].values():
                    # check whether the path over the edge start -> end is shorter than the previous known path to end
                    if self.distance[start] + edge.weight < self.distance[edge.end.value]:
                        # Update the distance to end and ends predecessor
                        self.distance[edge.end.value] = self.distance[start] + edge.weight
                        self.predecessors[edge.end.value] = start
                        found_better_distance[edge.end.value] = True
                    else:
                        found_better_distance[edge.end.value] = False
            # break if we haven't found a better option in our current iteration
            if True not in found_better_distance:
                break
        # only check for negative cycles if we had an improvement in our last iteration
        if True in found_better_distance:
            # check for negative cycles
            for start in self.graph.vertexes:
                for edge in self.graph.edges[start].values():
                    if self.distance[start] + edge.weight < self.distance[edge.end.value]:
                        print(f"The Edge {edge} is part of a negative circle!")
                        break
        return self.distance, self.predecessors
