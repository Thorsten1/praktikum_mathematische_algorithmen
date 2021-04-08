import sys

from Graph_Database.graph import Graph

if __name__ == '__main__':
    if len(sys.argv) == 0:
        print("Please provide the path to the import file")
        exit(1)
    graph = Graph(0)
    graph.import_from_file(sys.argv[1])
    graph.breadth_first_search()
