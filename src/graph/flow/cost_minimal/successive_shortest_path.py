from .abstractFlowCostmin import AbstractCostminFlow
from ..flow import residual_graph, Flow
from ...graph import timeit
from ...shortest_path.mooreBellmanFord import MooreBellmanFord


class SuccessiveShortestPath(AbstractCostminFlow):
    """
    """

    def __call__(self):
        """
        """
        return self._successive_shortest_path()

    @timeit
    def _successive_shortest_path(self) -> (bool, Flow):
        """
        :param int start: The start of our flow
        :param int target: The end of our flow
        :return The maximum flow
        """
        s_vertexes = []
        t_vertexes = []
        balance = 0
        # Initialisation
        for vertex in self.graph.vertexes.values():
            balance += vertex.balance
            if not vertex.edges:
                continue
            for edge in vertex.edges:
                # set flow to 0 for all edges with positive costs
                if edge.weight >= 0:
                    edge.flow = 0
                # if costs are negative set to maximum flow
                else:
                    edge.flow = edge.capacity
        # if the graph is not balanced we can stop here
        if balance != 0:
            print("The sinks require more units then the sources can provide.")
            return False, self.graph

        while True:
            """
            Step 1:
            Determine Residual Graph
            Choose s with b(s) - b'(s) > 0
            Choose t that is reachable from s where b(t) - b'(t) < 0
            """
            # get residual graph
            g_f = residual_graph(self.graph)
            # calculate b' values
            for edge in edge_list(g_f.edges):
                if edge.residual:
                    # only use residual edges and invert the behavior
                    g_f.vertexes[edge.start].balance -= edge.capacity
                    g_f.vertexes[edge.end].balance += edge.capacity
            # retrieve all vertexes where b(v) - b'(v) > 0
            s_vertexes = [v for v in g_f.vertexes.values() if self.graph.vertexes[v.value].balance - v.balance > 0]
            # retrieve all vertexes where b(s) - b'(s) < 0
            t_vertexes = [v for v in g_f.vertexes.values() if self.graph.vertexes[v.value].balance - v.balance < 0]
            # Cancel if there are no start points anymore
            if s_vertexes:
                # Choose a source vertex
                start = s_vertexes[0].value
                # determine all possible shortest paths to the other vertexes
                mbf = MooreBellmanFord(graph=g_f)
                distances, predecessors = mbf(start)
                # choose a sink vertex
                end = None
                for v in t_vertexes:
                    # Choose a vertex from t_vertexes that is reachable from
                    if distances[v.value] != float('Inf'):
                        end = v
                        break
                if end is None:
                    print(f"There is no s-t-Way from s {start} to any t in {t_vertexes}")
                    return False, self.graph
                p = []
                """
                Step 2:
                Determine a shortest s-t path within the residualgraph
                """
                curr = end.value
                # determine the path by traversing all predecessors
                while curr != start:
                    p.append(g_f.get_edge(predecessors[curr], curr))
                    curr = predecessors[curr]
                ymin = min(min(map(lambda e: e.capacity, p)), (self.graph.vertexes[start].balance - g_f.vertexes[start].balance), abs(self.graph.vertexes[end].balance - g_f.vertexes[end].balance))
                for pe in p:
                    if not pe.residual:
                        self.graph.edges[pe.start][pe.end].flow += ymin
                    else:
                        self.graph.edges[pe.end][pe.start].flow -= ymin
                """
                Break Condition:
                if b(v)-b'(v) is 0 for every vertex we have our costminimal flow otherwise fail
                """
            elif t_vertexes:
                # This case should never occur due to the first check within the initialisation
                print("The sinks require more units then the sources can provide.")
                return False, self.graph
            else:
                # determine the overall balance
                for v in g_f.vertexes.values():
                    if self.graph.vertexes[v.value].balance - v.balance != 0:
                        print("The balance b(v)-b'(v) isn't 0 for every vertex v.")
                        return False, self.graph
                self.cost = sum(map(lambda e: e.weight * e.flow, edge_list(self.graph.edges)))
                return True, self.graph


def edge_list(edge_dict: dict):
    """
    Transform the edge 2d dict into a list
    :param edge_dict: The dictionary of all edges
    :return: list of all edges
    """
    edge_list = []
    for s in edge_dict.values():
        if s:
            edge_list.extend(s.values())
    return edge_list
