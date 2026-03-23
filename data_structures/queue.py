"""
    Queue is an abstract data structure, somewhat similar to Stacks.
    Unlike stacks, a queue is open at both its ends. One end is always used to
    insert data (enqueue) and the other is used to remove data (dequeue).
    Queue follows First-In-First-Out methodology, i.e., the data item stored
    first will be accessed first.

    link: https://www.tutorialspoint.com/data_structures_algorithms/dsa_queue.htm
"""

class Queue:
    def __init__(self):
        self.items = list()

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        q = "< "
        for item in self.items:
            q += f"{item} "
        q += "<"
        return q

    def enqueue(self, item):
        """
        Add an item to the back of the queue
        Time Complexity: O(1)
        """
        self.items.append(item)

    def dequeue(self):
        """
        Remove an item from the front of the queue
        """
        try:
            return self.items.pop(0)
        except IndexError:
            raise IndexError("Pop from empty queue")

    def peek(self):
        return self.items[0] if self.items else None

    def isEmpty(self):
        return not self.items
