import heapq
import math

from graph.graph import Vertex, timeit
from graph.shortest_path.abstractShortestPath import ShortestPath


class Node:
    def __init__(self,
                 vertex: Vertex,
                 predecessor: Vertex,
                 distance: float = math.inf
                 ):
        self.vertex = vertex
        self.predecessor = predecessor
        self.distance = distance

    def __lt__(self, other):
        return self.distance < other.distance


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
        self.distance = [math.inf for _ in range(self.graph.vertex_count)]
        self.predecessors = [None for _ in range(self.graph.vertex_count)]

        # Initialize the list of remaining vertexes to visit, which will be used
        # as heapqueue, a sorted list, having the node with the lowest priority
        # always first. However, the distance to the start vertex is zero, as
        # its the beginning of course.
        remaining = [Node(self.graph.vertexes.get(n), None, math.inf)
                     for n in range(self.graph.vertex_count)]
        heapq.heappush(remaining,
                       Node(self.graph.vertexes.get(start_vertex), None, 0))

        # Iterate over remaining vertexes until the remaining list is empty.
        while remaining:
            # From the list of remaining vertexes, get the one with the minimum
            # known distance. It will be removed from the remaining list.
            cur = heapq.heappop(remaining)
            if self.distance[cur.vertex.value] != math.inf:
                continue

            # Persist the distance and predecessor of this vertex in the global
            # variabled returned at the end of the method, as its values won't
            # change anymore.
            self.distance[cur.vertex.value] = cur.distance
            self.predecessors[cur.vertex.value] = cur.predecessor

            # Iterate over all connected vertexes not known yet and update the
            # related distances, if these are better than the existing ones.
            for e in cur.vertex.edges:
                if self.distance[e.end.value] == math.inf:
                    if e.weight < 0:
                        print('Negative Kante im Graphen. Das Ergebnis ist ' +
                              ' ggf. nicht optimal!')

                    heapq.heappush(remaining,
                                   Node(e.end,
                                        cur.vertex,
                                        cur.distance + e.weight))

        return self.distance, self.predecessors
