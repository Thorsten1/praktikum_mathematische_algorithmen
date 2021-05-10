import math

from graph.graph import Graph, Vertex, timeit
from graph.tsp.abstractTSP import TSP


class BruteForce(TSP):
    def __init__(self):
        """
        Constructor.
        """
        self.min_cost = math.inf
        self.min_path = []

        super().__init__()

    def __call__(self, start: int = 0) -> float:
        """
        Get the minimal cost for a TSP route.


        :param start: ID of the :py:class:`.Vertex` to start from.

        :returns: Cost of the minimal TSP route.
        """
        # Calculate the minimal TSP route by calling the internal methods, which
        # in fact are just wrappers to measure the time spent on calculations.
        self.__timeHelper(self.graph.vertexes.get(start))

        # TODO: If required by other methods and external callees, a graph
        #       including just the TSP route could be calculated from 'min_path'
        #       here.

        # Return the cost of the minimal route calculated above. It can't be
        # returned directly from the function, as its using recursion and can't
        # reliable determine when a global minimum is reached during runtime.
        return self.min_cost

    @timeit
    def __timeHelper(self,
                     vertex: Vertex,
                     path: list[Vertex] = [],
                     distance: float = 0.0
                     ) -> None:
        """
        Timed version of :py:meth:`_run`.

        This wrapper of :py:meth:`_run` uses the global :py:func:`.timeit`
        wrapper to get the runtime of this algorithm.
        """
        self._run(vertex, path, distance)

    def _run(self,
             vertex: Vertex,
             path: list[Vertex] = [],
             distance: float = 0.0
             ) -> None:
        """
        Determine a minimal round trip using bruteforce.


        :param vertex: :py:class:`.Vertex` to start from.
        :param path: Vertexes already visited.
        :param distance: Commulated distance of the vertexes already visited.

        :return: The Graph for the round trip.
        """
        # Add the current vertex to the ones already visited before recursing
        # any further to traverse the graph.
        path.append(vertex)

        # If this invocation of the method doesn't have visited all vertexes of
        # the graph yet, iterate over the conneected vertexes of the current one
        # to  further explore the graph and get an optimal TSP route.
        #
        # NOTE: On recursion, copies of local variables need to be used to not
        #       just pass references, which would alter the current scope on
        #       writes and make recursions to other nodes impossible.
        if len(path) < len(self.graph.vertexes):
            for e in vertex.edges:
                if e.end not in path:
                    self._run(e.end, list(path), distance + e.weight)

        else:
            # If the node visited is the last remaining of the graph not visited
            # yet, add another edge and its weight to close the route back to
            # the starting point.
            finEdge = next(filter(lambda e: e.end == path[0], vertex.edges))
            distance = distance + finEdge.weight

            # If the distance calculated is a new global minimum, update the
            # global variables with its successors.
            if distance < self.min_cost:
                self.min_cost = distance
                self.min_path = path
