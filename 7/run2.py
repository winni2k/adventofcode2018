from heapq import heapify, heappop, heappush

import attr
import networkx as nx

lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()
lines = open('input.txt').readlines()


@attr.s(slots=True)
class Worker:
    letter = attr.ib('')
    time_left = attr.ib(0)
    base_time = attr.ib(0)

    def tick(self):
        self.time_left -= 1

    def put(self, letter):
        self.letter = letter
        self.time_left = self.base_time + ord(letter) - ord('A') + 1

    def get(self):
        if self.time_left == 0:
            return self.letter
        else:
            return None

    def is_idle(self):
        if self.time_left < 1:
            return True
        return False


graph = nx.DiGraph()
for line in lines:
    fields = line.split()
    graph.add_edge(fields[1], fields[7])

start_nodes = {pair[0] for pair in filter(lambda pair: len(pair[1]) == 0,
                                          [(n, list(graph.in_edges(n))) for n in graph])}
available = list(start_nodes)
heapify(available)
output = []
workers = [Worker(base_time=60) for _ in range(5)]
clock = -1
while len(output) != len(graph):
    clock += 1
    for worker in workers:
        worker.tick()
    for chosen in filter(None, (w.get() for w in workers)):
        output.append(chosen)
        for child in graph.successors(chosen):
            if child not in available and child not in output and all(
                p in output for p in graph.predecessors(child)):
                heappush(available, child)
    for worker in filter(lambda w: w.is_idle(), workers):
        if len(available) != 0:
            worker.put(heappop(available))

print(clock)
