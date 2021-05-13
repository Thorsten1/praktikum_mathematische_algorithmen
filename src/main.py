#!/usr/bin/env python

import argparse

from graph.graph import Graph
from graph.mst.kruskal import Kruskal
from graph.mst.prim import Prim
from graph.shortest_path.mooreBellmanFord import MooreBellmanFord
from graph.tsp.branchAndBound import BranchAndBound
from graph.tsp.bruteForce import BruteForce
from graph.tsp.doubleTree import DoubleTree
from graph.tsp.nearestNeighbour import NearestNeighbour


def getArgs() -> argparse.Namespace:
    """
    Parse command line arguments.

    This function parses the application's command line arguments and returns
    the :py:class:`argparse.Namespace` to access the passed argument values. If
    necessary, this function emits a usage message and raises an error on
    invalid arguments or values.


    :returns: A :py:class:`argparse.Namespace` to access the argument values.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('graph',
                        help='graph file to load')
    parser.add_argument('-m', '--moore_bellman_ford',
                        action='store_true',
                        help='Use the Moore-Bellman-Ford Algorithm to determine shortest paths')
    parser.add_argument('-k', '--kruskal',
                        action='store_true',
                        help='Use the Kruskal algorithm to declare an MSTs cost')
    parser.add_argument('-p', '--prim',
                        action='store_true',
                        help='Use the Prim algorithm to declare an MSTs cost')

    parser.add_argument('-n', '--nearestneighbour',
                        action='store_true',
                        help='Use nearest Neighbour to determine an optimal round trip')
    parser.add_argument('-d', '--doubletree',
                        action='store_true',
                        help='Use Double-Tree Algorithm to determine an optimal round trip')
    parser.add_argument('-bf', '--bruteforce',
                        action='store_true',
                        help='Use bruteforce to determine an optimal round trip')
    parser.add_argument('-bb', '--branchAndBound',
                        action='store_true',
                        help='Use Branch&Bound Algorithm to determine an optimal round trip')

    # Parse the command line arguments and return the generated namespace. If
    # an argument is unknown, or its value does not match the specification, an
    # error message will be generated and the help message shown.
    return parser.parse_args()


if __name__ == '__main__':
    # Parse the command line arguments. If necessary, this function will print
    # error messages and exits the application on errors.
    args = getArgs()

    if args.moore_bellman_ford:
        graph = MooreBellmanFord()
        graph.import_from_file(args.graph)
        print(graph())

    elif args.kruskal:
        mst = Kruskal()
        mst.import_from_file(args.graph)
        print(mst())

    elif args.prim:
        mst = Prim()
        mst.import_from_file(args.graph)
        print(mst())

    elif args.nearestneighbour:
        tsp = NearestNeighbour()
        tsp.import_from_file(args.graph)
        print(tsp().overall_weight)

    elif args.doubletree:
        tsp = DoubleTree()
        tsp.import_from_file(args.graph)
        print(tsp().overall_weight)

    elif args.bruteforce:
        tsp = BruteForce()
        tsp.import_from_file(args.graph)
        tsp()
        print(tsp.min_cost)

    elif args.branchAndBound:
        tsp = BranchAndBound()
        tsp.import_from_file(args.graph)
        tsp()
        print(tsp.min_cost)

    else:
        graph = Graph()
        graph.import_from_file(args.graph)
        graph.component_time()
