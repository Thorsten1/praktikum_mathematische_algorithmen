#!/usr/bin/env python

import argparse

from graph.graph import Graph


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

    # Parse the command line arguments and return the generated namespace. If
    # an argument is unknown, or its value does not match the specification, an
    # error message will be generated and the help message shown.
    return parser.parse_args()


if __name__ == '__main__':
    # Parse the command line arguments. If necessary, this function will print
    # error messages and exits the application on errors.
    args = getArgs()

    graph = Graph(0)
    graph.import_from_file(args.graph)
    print(graph)
