"""
The Problem It Solves
Imagine you're building a network of computers. You connect them one pair at a time. At any point someone asks: "Are computer A and computer Z on the same network?"
You could run BFS/DFS every time someone asks — but that's O(N + E) per query. If you have millions of computers and billions of queries, that's unacceptable.
Union-Find answers that question in nearly O(1) per operation, regardless of how large the network grows. That's its entire reason for existing — dynamic connectivity at scale.

The Core Idea
Every node belongs to exactly one group. Each group has a representative node called the root or parent. To check if two nodes are in the same group, you find both of 
their roots and compare. If the roots are the same — same group. Think of it like company org charts. Every employee ultimately reports to one CEO.
To check if two employees work for the same company, trace both up to their CEO. Same CEO — same company.

The Two Operations
1. Find(x) — returns the root/representative of x's group. Trace parent pointers up until you reach a node that is its own parent.
2. Union(x, y) — merges the groups containing x and y into one group. Find both roots, then make one root point to the other.

That's it. The entire data structure is just these two operations.

The Internal Representation

Union-Find is typically implemented as an array (or dictionary) called parent where parent[i] stores the parent of node i.

Initially every node is its own parent — N isolated groups:
```
parent = [0, 1, 2, 3, 4]
           ↑  ↑  ↑  ↑  ↑
    each node points to itself
```

After union(0, 1):
parent = [1, 1, 2, 3, 4]
    node 0 now points to node 1
    node 1 is the root of that group

After union(1, 2):
parent = [1, 2, 2, 3, 4]
    group containing 0, 1, 2 — root is 2

find(0) → follows 0 → 1 → 2. Returns 2.
find(3) → returns 3. Different root, different group.

The Naive Problem
Without optimizations, this degrades badly. Consider unioning nodes in a chain: union(0,1), union(1,2), union(2,3), union(3,4). Your tree becomes a straight line:
0 → 1 → 2 → 3 → 4
find(0) now traverses the entire chain — O(N). You've rebuilt the worst case of a linked list. Union-Find without optimizations is no better than a naive approach.
This is why two optimizations are non-negotiable. You must know both.

Optimization 1: Union by Rank
The problem: when merging two groups, which root becomes the new root? Naively you pick arbitrarily, which can create tall trees.
The fix: always attach the shorter tree under the taller tree. Track the rank (approximate height) of each tree. When unioning,
the root with lower rank points to the root with higher rank. If ranks are equal, pick either and increment the winner's rank by 1.

This guarantees tree height never exceeds O(log N).
rank = [0, 0, 0, 0, 0]  # initially all zero

union(0, 1):
    both rank 0 → make 0 point to 1, increment rank[1]
    parent = [1, 1, 2, 3, 4]
    rank   = [0, 1, 0, 0, 0]

union(2, 3):
    both rank 0 → make 2 point to 3, increment rank[3]
    parent = [1, 1, 3, 3, 4]
    rank   = [0, 1, 0, 1, 0]

union(1, 3):
    both rank 1 → make 1 point to 3, increment rank[3]
    parent = [1, 3, 3, 3, 4]
    rank   = [0, 1, 0, 2, 0]
Tree stays balanced. find stays fast.

Optimization 2: Path Compression
The problem: even with union by rank, find still traverses multiple hops to reach the root.
The fix: after find(x) traverses up to the root, go back and make every node on that path point directly to the root. Future calls on those nodes are now O(1).
Before find(0):
0 → 1 → 3 (root)

After find(0) with path compression:
0 → 3 (direct)
1 → 3 (direct)
This happens automatically during find — no extra pass needed. One line of code: after finding the root recursively, set parent[x] = root before returning.

Combined Complexity
With both optimizations together, each operation runs in O(α(N)) — where α is the inverse Ackermann function. This grows so slowly that for any 
practical input size (even 10^80 nodes), α(N) ≤ 4. It's effectively constant time. This is one of the most elegant results in computer science —
a seemingly complex problem reduced to near-constant time through two simple tricks.

Where It Shows Up In Interviews
1. Cycle detection in undirected graphs — when you union two nodes that already share a root, you've found a cycle. Cleaner than DFS for this specific use case.
2. Number of connected components — count how many distinct roots exist after processing all edges.
3. Kruskal's Minimum Spanning Tree — sort edges by weight, add each edge if the two nodes don't already share a root (Union-Find prevents cycles). Your topological sort knowledge plus Union-Find gives you Kruskal's almost for free.
4. Dynamic connectivity problems — "as connections are added, are these two nodes connected?" Classic Union-Find.
5. LeetCode patterns — any problem involving merging groups, friend circles, island counting with dynamic additions, or redundant connections is likely Union-Find.
"""

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0 for i in range(n)]

    def __repr__(self):
        return f"parent: {self.parent}, rank: {self.rank}"

    def find(self, x):
        """
        Find with path compression
        """
        if x >= len(self.parent):
            raise ValueError(f"node {x} does not exist")

        return self._find(x, self.parent)

    def _find(self, x, parent):
        if parent[x] == x:
            return x

        root = self._find(parent[x], parent)
        parent[x] = root
        return root

    def union(self, x, y):
        """
        returns True if merged, False if already same group
        """
        if x < 0 or x >= len(self.parent):
            raise ValueError(f"node {x} does not exist")

        if y < 0 or y >= len(self.parent):
            raise ValueError(f"node {y} does not exist")
    
        if self.find(x) == self.find(y):
            return False

        # Check rank and merge
        if self.rank[y] > self.rank[x]:
            self.parent[x] = y
            # No need to increament rank since rank of y is already higher
        elif self.rank[y] == self.rank[x]:
            self.parent[x] = y
            self.rank[y] += 1
        else:
            self.parent[y] = x
            self.rank[x] += 1

        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def component_count(self):
        distinct = 0
        for idx, value in enumerate(self.parent):
            if idx == value:
                distinct += 1

        return distinct
