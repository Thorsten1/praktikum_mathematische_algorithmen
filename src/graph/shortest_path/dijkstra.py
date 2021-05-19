import math

from graph.graph import timeit
from graph.shortest_path.abstractShortestPath import ShortestPath


class Dijkstra(ShortestPath):
    def __init__(self):
        super().__init__()

    def __call__(self, start_vertex: int):
        return self._dijkstra(start_vertex)

    @timeit
    def _dijkstra(self, start_vertex: int) -> tuple[list, list]:
        """
        Execute the Dijkstra Algorithm from the provided start vertex

        :param start_vertex: The Vertex from where to start
        :return: Two lists of distances and predecessors
        """
        # initialize the distances with infinity and their predecessors with
        # None because they aren't known yet
        self.distance = {n: math.inf for n in range(self.graph.vertex_count)}
        self.predecessors = [None for _ in range(self.graph.vertex_count)]

        # Iterate over remaining vertexes until the remaining list is empty. The
        # list of remaining vertexes is initialized by a full copy of distances
        # as none has been visited before. However, the distance to the start
        # vertex is zero, as ... its the beginning of course.
        self.distance[start_vertex] = 0
        remaining = self.distance.copy()
        while remaining:
            # From the list of remaining vertexes, get the one with the minimum
            # known distance. It will be removed from the remaining list and its
            # final distance copied into the  return dictionary.
            cur = self.graph.vertexes.get(min(remaining, key=remaining.get))
            self.distance[cur] = remaining[cur]
            del remaining[cur]

            # Iterate over all connected vertexes not known yet and update the
            # related distances, if these are better than the existing ones.
            for e in cur.edges:
                if e.end in remaining:
                    if e.weight < 0:
                        print('Negative Kante im Graphen. Das Ergebnis ist ' +
                              ' ggf. nicht optimal!')

                    tmp = self.distance[cur] + e.weight
                    if tmp < remaining[e.end]:
                        remaining[e.end] = tmp
                        self.predecessors[e.end.value] = cur.value

        return self.distance.values(), self.predecessors
