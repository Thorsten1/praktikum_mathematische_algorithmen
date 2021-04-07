from queue import Queue
from typing import Union


class Vertex:
    def __init__(self, value: int, edges=None, degree=None):
        self.value = value
        self.__name__ = str(value)
        self.edges = edges if edges is not None else {}
        self.degree = degree if degree is not None else self.edges.__len__()
        self._set_loop()

    def __eq__(self, o: Union[int, object]):
        if isinstance(o, int):
            return self.value == o
        elif isinstance(o, Vertex):
            return self.value == o.value

    def add_edge(self, edge):
        self.edges[edge.end.value] = edge
        self.degree = self.degree + 1

    def _set_loop(self):
        if self.value in self.edges:
            self.loop = True

    def __str__(self):
        return f"{self.value}: {self.edges}"

    def __repr__(self):
        return f"{self.value}: {self.edges}"


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
        start_v = self.vertexes.get(start, Vertex(value=start))
        end_v = self.vertexes.get(end, Vertex(value=end))
        start_v.add_edge(Edge(start_v, end_v, weight))
        if self.directed:
            end_v.add_edge(Edge(start_v, end_v, weight))
        else:
            end_v.add_edge(Edge(end_v, start_v, weight))
        self.vertexes[start_v.value] = start_v
        self.vertexes[end_v.value] = end_v

    def __str__(self):
        return f"{self.vertex_count}: {str(self.vertexes)}"

    def import_from_file(self, filepath):
        with open(filepath, "r") as input_file:
            self.vertex_count = int(input_file.readline())
            for knot in input_file.readlines():
                s, e = knot.split("\t")
                self.add_edge(int(s), int(e))

    def breadth_first_search(self):
        """
        Check whether the graph is connected and report the number of connected components
        :return:
        """
        queue = Queue()
        queue.put(self.vertexes[0])
        marked = {self.vertexes[0].value: True}
        while queue.qsize() > 0:
            current_vertex: Vertex = queue.get()
            # iterate through all neighbour vertexes
            for vertex in [_.end for _ in current_vertex.edges.values()]:
                if marked.get(vertex.value):
                    continue
                queue.put(vertex)
                marked = {vertex.value: True}
        return False
