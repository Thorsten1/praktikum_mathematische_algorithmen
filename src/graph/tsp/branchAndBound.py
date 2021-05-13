from graph.graph import Vertex

from .bruteForce import BruteForce


class BranchAndBound(BruteForce):
    """
    Branch and Bound TSP route algorithm.

    Branch and Bound is essentially the same as :py:class:`.BruteForce` with a
    small optimization to abort routes, which can't be a global minimum, before
    investing further efforts in calculating these ones.
    """

    def _run(self,
             vertex: Vertex,
             path: list[Vertex] = [],
             distance: float = 0.0
             ) -> None:
        """
        Determine a minimal round trip using Branch and Bound algorithm.


        :return: The Graph for the round trip.
        """
        # If the distance exceeds the global minimum, abort following this
        # branch and try another one by brute force instead.
        if distance < self.min_cost:
            super()._run(vertex, path, distance)
