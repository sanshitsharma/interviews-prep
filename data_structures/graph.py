"""
A graph is a set of nodes (also called vertices) connected by edges. That's it. Everything else is a variation on that definition.
Graphs model relationships. A tree is actually a special case of a graph — acyclic, connected, with one root. Once you remove those constraints, you have a general graph.

Key vocabulary you must be fluent with:
- Directed vs Undirected. In an undirected graph, an edge between A and B means you can travel both ways. In a directed graph (digraph), an edge from A → B does not imply B → A. Twitter follows are directed. Facebook friendships are undirected.
- Weighted vs Unweighted. Edges can carry a cost/weight. Road distances, latency between servers, flight costs. Unweighted graphs treat all edges as equal.
- Cyclic vs Acyclic. A cycle means you can start at a node, follow edges, and return to where you started. A DAG — Directed Acyclic Graph — is one of the most important graph types in interviews. Dependency graphs, build systems, task scheduling are all DAGs.
- Connected vs Disconnected. A connected graph has a path between every pair of nodes. A disconnected graph has isolated components — islands with no edges between them.
- In-degree / Out-degree. For a node in a directed graph, in-degree is the number of edges coming in, out-degree is edges going out. Critical concept for topological sort.
- Dense vs Sparse. A dense graph has many edges relative to nodes — close to the maximum possible edges. A sparse graph has few edges. This distinction directly drives which implementation you choose.
"""

from collections import deque

class Graph:
    def __init__(self, is_directed = False):
        self.adj_list = {}
        self.is_directed = is_directed

    def __repr__(self):
        return f"{self.adj_list}"

    def add_node(self, value, connections = None):
        self.adj_list[value] = list()
        for dest in (connections or []):
            if dest not in self.adj_list.keys():
                print(f"WARNING: destination node {dest} does not exist in graph. Skipping..")
                continue

            self.adj_list[value].append(dest) 
            if not self.is_directed:
                self.adj_list[dest].append(value)
    
    def add_edge(self, src, dest):
        if not src in self.adj_list or not dest in self.adj_list:
            raise ValueError("one or more nodes does not exist in graph")

        if dest in self.adj_list[src]:
            return

        self.adj_list[src].append(dest)
        if not self.is_directed:
            self.adj_list[dest].append(src)

    def bft(self, start, visited = None):
        if start not in self.adj_list:
            raise ValueError(f"start node {start} does not exist in graph")

        q = deque() 
        q.append(start)
        nodes = list() # Will be returned

        if visited is None:
            visited = set() # nodes that have been visited
        visited.add(start)

        while q:
            curr = q.popleft()

            nodes.append(curr)

            for neighbor in self.adj_list[curr]:
                if neighbor not in visited:
                    q.append(neighbor)
                    visited.add(neighbor)

        return nodes

    def bft_all(self):
        visited = set()
        all_nodes = list()

        for node in self.adj_list:
            if node not in visited:
                all_nodes.extend(self.bft(node, visited))

        return all_nodes

    def dft(self, start, visited = None):
        if start not in self.adj_list:
            raise ValueError(f"start node {start} does not exist in graph")

        if visited is None:
            visited = set()

        nodes = list()

        self._dft(start, visited, nodes)
        return nodes

    def _dft(self, curr, visited, nodes):
        if curr in visited:
            return

        visited.add(curr)
        nodes.append(curr)

        for neighbor in self.adj_list[curr]:
            self._dft(neighbor, visited, nodes)

    def dft_all(self):
        visited = set()
        all_nodes = []

        for node in self.adj_list:
            if node not in visited:
                all_nodes.extend(self.dft(node, visited))

        return all_nodes

    def has_cycle(self):
        visited = set()

        for node in self.adj_list:
            if node not in visited:
                if self.is_directed:
                    rec_stack = set()
                    if self._has_cycle_directed(node, visited, rec_stack):
                        return True
                else:
                    if self._has_cycle_undirected(node, visited, None):
                        return True

        return False

    def _has_cycle_directed(self, curr, visited, rec_stack):
        if curr in visited:
            # if a node has been visited before, it's processed. Nothing to do here anymore
            return False

        if curr in rec_stack:
            # rec_stack tracks nodes on the CURRENT active DFS path (call stack).
            # If a neighbor is in rec_stack, we've found a back edge — a path
            # leading back to an ancestor we're still processing. That's a cycle.
            return True

        visited.add(curr)
        rec_stack.add(curr)

        for neighbor in self.adj_list[curr]:
            if self._has_cycle_directed(neighbor, visited, rec_stack):
                return True

        rec_stack.remove(curr)
        return False

    def _has_cycle_undirected(self, curr, visited, parent):
        if curr in visited:
            # if a node has been visited before, it's processed. Nothing to do here anymore
            return False

        visited.add(curr)
        for neighbor in self.adj_list[curr]:
            if neighbor == parent:
                # If the neighbor is the parent node, then we just came from here. That doesn't mean 
                # we have a cycle. Nothing to do just continue.
                continue
            elif neighbor in visited:
                # If the neighbor is not the parent but has been visited before, it means we have explored
                # that node before from another route. It means there is a cycle. 
                return True
            elif self._has_cycle_undirected(neighbor, visited, curr):
                # Nothing conclusive yet. Just continue recursion
                return True

        return False

    def topological_sort(self):
        """
        Topological sort is a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u → v, 
        vertex u appears before v in the ordering. It’s widely used in task scheduling, dependency resolution, and build systems.
        It is not possible for graphs with cycles or undirected edges.
        """
        if not self.is_directed:
            raise TypeError("Topological sort is not supported for undirected graphs")

        q = deque()
        result = []

        # Find all nodes with in-degree 0 and add them to the queue
        indegree_map = {node: 0 for node in self.adj_list}
        for node in self.adj_list:
            for neighbor in self.adj_list[node]:
                indegree_map[neighbor] += 1

        for node, indegree in indegree_map.items():
            if indegree == 0:
                q.append(node)

        while q:
            curr = q.popleft()
            result.append(curr)
            for neighbor in self.adj_list[curr]:
                indegree_map[neighbor] -= 1
                if indegree_map[neighbor] == 0:
                    q.append(neighbor)

        if len(result) == len(self.adj_list):
            return result

        raise ValueError("cycles detected in graph. topological sort not possible")
                

