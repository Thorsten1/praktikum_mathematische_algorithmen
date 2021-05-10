import functools
import time
from collections import deque
from typing import Union


def timeit(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsed_time * 1000)))
        return res

    return wrapped


class Vertex:
    def __init__(self, value: int, edges=None):
        self.value = value
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

    def __hash__(self):
        return self.value

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
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()


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

    def __lt__(self, o):
        """
        Compare the weight of Edges

        :param o: Value to compare with, either Edge or int
        :return: bool Value whether the own weight is less then the other value  (self < o)
        """
        if isinstance(o, Edge):
            return self.weight < o.weight
        if isinstance(o, int):
            return self.weight < o
        return False

    def __le__(self, o):
        """
        Compare the weight of Edges

        :param o: Value to compare with, either Edge or int
        :return: bool Value whether the own weight is less then or equal to the other value  (self <= o)
        """
        if isinstance(o, Edge):
            return self.weight <= o.weight
        if isinstance(o, int):
            return self.weight <= o
        return False

    def __gt__(self, o):
        """
        Compare the weight of Edges

        :param o: Value to compare with, either Edge or int
        :return: bool Value whether the own weight is greater then the other value  (self < o)
        """
        if isinstance(o, Edge):
            return self.weight > o.weight
        if isinstance(o, int):
            return self.weight > o
        return False

    def __ge__(self, o):
        """
        Compare the weight of Edges

        :param o: Value to compare with, either Edge or int
        :return: bool Value whether the own weight is greater then or equal to the other value  (self <= o)
        """
        if isinstance(o, Edge):
            return self.weight >= o.weight
        if isinstance(o, int):
            return self.weight >= o
        return False

    def __str__(self):
        if self.weight == 0:
            return f"{self.start} -> {self.end}"
        return f"{self.start} -({self.weight})-> {self.end}"

    def __eq__(self, o):
        return hash(o) == self.__hash__()

    def __repr__(self):
        self.__str__()

    def __hash__(self):
        return hash(f"{self.start.value}:{self.end.value}")

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
    def __init__(self, vertex_count=0, directed=False, vertexes=None, weighted=False):
        self.vertex_count = vertex_count
        self.vertexes = vertexes if vertexes is not None else {}
        self.directed = directed
        self.weighted = weighted
        self.edges = set()

    def add_existing_edge(self, edge: Edge):
        """
        Add an edge to the Graph as well as the vertexes if not yet present
        This will not take the old vertexes but generate new ones to strip them from theire edges
        :param edge: The edge that shall be added
        :return: void
        """
        # Generate a new edge and new vertexes so they aren't related to the old graph
        if not self.vertexes.get(edge.start.value):
            self.vertexes[edge.start.value] = Vertex(edge.start.value)
        if not self.vertexes.get(edge.end.value):
            self.vertexes[edge.end.value] = Vertex(edge.end.value)
        self.add_edge(edge.start.value, edge.end.value, edge.weight)

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

        # Create a new edge object and add it to the internal list of edges.
        # Although it is not required for operating on graphs, it will be used
        # for optimized performance and avoid iterating over all vertexes.
        edge = Edge(start_v, end_v, weight)
        self.edges.add(edge)

        # Add the edge to its start vertex, allowing the vertex to know its
        # adjacent vertexes. For undirected graphs, the end vertex will get an
        # edge of opposite direction, too.
        start_v.add_edge(edge)
        if not self.directed:
            end_v.add_edge(Edge(end_v, start_v, weight))

    def __str__(self):
        return f"{self.vertex_count}: {str(self.vertexes)}"

    @property
    def overall_weight(self) -> float:
        """
        Returns the overall weight of all edges within the Graph.
        Mostly used for TSP method

        :return: The weight of all edges
        """
        if not self.weighted:
            return 0
        return sum([_.weight for _ in self.edges])

    @timeit
    def import_from_file(self, filepath):
        with open(filepath, "r") as input_file:
            self.vertex_count = int(input_file.readline())
            for i in range(self.vertex_count):
                self.vertexes[i] = Vertex(value=i)
            for knot in input_file:
                s, e = knot.split("\t")
                self.add_edge(int(s), int(e))

    @property
    def components(self) -> int:
        """
        Get the number of components for this graph.

        This method dynamically calculates the number of components for this
        graph by counting the search operations required on this graph, until
        all vertexes have been marked by the search algorithm.


        :returns: Number of components for this graph.
        """
        # Iterate over the vertexes of this graph and run a search algorithm
        # originating from each of them. As the search algorithm updates the
        # vertexes marked, following iterations will ignore these nodes, so each
        # iteration is equivalent to a component of the graph.
        #
        # NOTE: Using lambda functions usually introduces some overhead for
        #       calling 'other' functions. However, as filter functions don't
        #       write data but just return a binary result, even large datasets
        #       didn't show a decreased performance compared to iterating over
        #       all items with checking the marked status inside the loop.
        components = 0
        marked: set[int] = set()
        for i in filter(lambda x: x not in marked, self.vertexes):
            # Start a search operation originating from the current vertex, but
            # don't give it a needle to search to force it traversing the whole
            # component of the graph this vertex belongs to. After increasing
            # the component counter, the operation will be repeated with the
            # next unmarked vertex, until all vertexes have been marked.
            self.bfs(-1, self.vertexes[i], marked)
            components += 1

        return components

    def bfs(self, needle: int, start: Vertex, marked: set[int] = None) -> bool:
        """
        Search ``needle`` in this graph by using a breath-first-search (BFS).

        This method implements searching a ``needle`` in this graph by using a
        breath-first-search (BFS) algorithm originating from :py:class:`.Vertex`
        ``start``.

        .. note:: This method is optimized to be used by :py:meth:`components`.
            As the current goal is speed optimization, this method doesn't
            implement the actual comparison of vertex values yet.


        :param needle: The needle to search.
        :param start: At which :py:class:`.Vertex` to start the search.
        :param marked: An optional set identifying the vertexes already visited
            and marked to be ignored in further search operations. By not
            passing this argument, the search operation will start from scratch.
            As python usually passes by reference, passing an empty set to this
            parameter can be used to get the vertexes visited, too.

        :returns: A boolean indicating whether ``needle`` has been found in this
            graph or not.
        """
        # If no marked vertexes have been passed, start this search operation
        # from scratch by creating an empty marked set.
        if marked is None:
            marked = set()

        # Initialize the search queue with the first vertex as starting point
        # and mark it as visited to avoid loops during search.
        marked.add(start.value)
        queue = deque([start])

        # Run the vertex queue until no vertexes are left to be traversed. New
        # vertexes will be queued by the BFS algorithm in the loop's body and
        # visited in following iterations.
        while queue:
            # Iterate over the edges of the vertex to get its connected vertexes
            # and check them to match the needle or further searching starting
            # from them.
            #
            # NOTE: Due to the current implementation of the 'Vertex' class,
            #       this will iterate over both edges starting and ending at
            #       this vertex. For directed graphs, edges starting from the
            #       vertex should be stored separately to just iterate these
            #       below instead of all.
            for e in (queue.popleft()).edges:
                # TODO: As this method is optimized for getting the components
                #       of a graph, no actual search will be done. Therefore, to
                #       get a working BFS, one needs to uncomment the following
                #       lines of code:
                #
                #       if e.end.value == needle:
                #           return True

                # If the connected vertex doesn't match the needle, check if its
                # already has been marked as visited (or a visit is scheduled).
                # If so, no second visit is required.
                if e.end.value in marked:
                    continue

                # As this vertex likely was never seen before, it should be
                # visited by the search algorithm and will be enqueued. It is
                # marked as visited to avoid further vertex operations to
                # enqueue the same vertex twice.
                marked.add(e.end.value)
                queue.append(e.end)

        # If the method didn't return yet, the search didn't succeed and needle
        # couldn't be found in the component of the graph, the start vertex does
        # belong to.
        return False

    @timeit
    def component_time(self):
        print(self.components)
