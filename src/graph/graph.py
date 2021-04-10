import functools
import time
from collections import deque
from typing import Union


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc


class Vertex:
    def __init__(self, value: int, edges=None):
        self.value = value
        self.__name__ = str(value)
        self.edges = edges if edges is not None else set()

    def __eq__(self, o: Union[int, object]) -> bool:
        """
        Compare vertex.

        This method compares the value of this vertex with integers passed. If
        an object of type :py:class:`.Vertex` is passed, its value will be
        compared instead.


        :param o: The object to be matched.

        :returns: Whether the passed object matches this vertex. Although
            objects of any type may be passed, this method statically returns
            false, if the passed type can't be handled by this vertex.
        """
        if isinstance(o, int):
            return self.value == o
        elif isinstance(o, Vertex):
            return self.value == o.value
        else:
            return False

    @property
    def degree(self) -> int:
        """
        Get degree of this vertex.

        This method returns the degree of a specific vertex by counting the
        edges connected to it.


        :returns: The degree of this vertex.
        """
        return len(self.edges)

    def add_edge(self, edge):
        self.edges.add(edge)

    def __str__(self):
        return f"{self.value}: {self.edges}"

    def __repr__(self):
        return f"{self.value}"


class Edge:
    def __init__(self, start: Vertex, end: Vertex, weight=0):
        """
        Describes edges between vertexes
        :param start: First vertex start if directed
        :param end: Second vertex end if directed
        :param weight: weight (0 if unweighted)
        """
        self.start = start
        self.end = end
        self.weight = weight

    def __str__(self):
        if self.weight == 0:
            return f"{self.start} -> {self.end}"
        return f"{self.start} -{self.weight}-> {self.end}"

    def __repr__(self):
        if self.weight == 0:
            return f"{self.start} -> {self.end}"
        return f"{self.start} -{self.weight}-> {self.end}"

    @property
    def is_loop(self) -> bool:
        """
        Check whether this edge is a loop.

        This method checks, whether the edge described by this edge object is a
        loop, i.e. its ``start`` and ``end`` match the same :py:class:`.Vertex`.


        :returns: Whether this edge is a loop.
        """
        return self.start == self.end


class Graph:
    def __init__(self, vertex_count: int, directed=False, vertexes=None, weighted=False):
        self.vertex_count = vertex_count
        self.vertexes = vertexes if vertexes is not None else {}
        self.directed = directed
        self.weighted = weighted

    def add_edge(self, start: int, end: int, weight=0):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        :param start:
        :param end:
        :param weight:
        :return: void
        """
        start_v = self.vertexes.get(start)
        end_v = self.vertexes.get(end)
        start_v.add_edge(Edge(start_v, end_v, weight))
        if self.directed:
            end_v.add_edge(Edge(start_v, end_v, weight))
        else:
            end_v.add_edge(Edge(end_v, start_v, weight))

    def __str__(self):
        return f"{self.vertex_count}: {str(self.vertexes)}"

    @timeit
    def import_from_file(self, filepath):
        with open(filepath, "r") as input_file:
            self.vertex_count = int(input_file.readline())
            for i in range(self.vertex_count):
                self.vertexes[i] = Vertex(value=i)
            for knot in input_file:
                s, e = knot.split("\t")
                self.add_edge(int(s), int(e))

    @timeit
    def breadth_first_search(self):
        """
        Check whether the graph is connected and report the number of connected components
        :return: number of components
        """
        marked = set()
        components = 0
        for vert in list(self.vertexes.values()):
            if vert.value in marked:
                continue
            marked.add(vert.value)
            queue = deque([vert])
            while queue:
                current_vertex: Vertex = queue.popleft()
                # iterate through all neighbour vertexes
                for vertex in [_.end for _ in current_vertex.edges]:
                    if vertex.value in marked:
                        continue
                    queue.append(vertex)
                    marked.add(vertex.value)
            components = components + 1
        print(components)
