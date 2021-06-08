from .abstractFlowMax import AbstractMaxFlow

from graph.graph import Edge, timeit


class EdmondsKarp(AbstractMaxFlow):
    """
    """

    def __call__(self, start, target):
        """
        """
        return self._edmondsKarp(start, target)

    @timeit
    def _edmondsKarp(self, start, target):
        """
        """
        pass
