from heapq import heapify, heappop, heappush

import networkx as nx

lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()
lines = open('input.txt').readlines()

graph = nx.DiGraph()
for line in lines:
    fields = line.split()
    graph.add_edge(fields[1], fields[7])

start_nodes = {pair[0] for pair in filter(lambda pair: len(pair[1]) == 0,
                                          [(n, list(graph.in_edges(n))) for n in graph])}
available = list(start_nodes)
heapify(available)
output = []
while len(output) != len(graph):
    chosen = heappop(available)
    output.append(chosen)
    for child in graph.successors(chosen):
        if child not in available and child not in output and all(p in output for p in graph.predecessors(child)):
            heappush(available, child)

print(''.join(output))
