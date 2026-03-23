#!/usr/bin/python

"""
    Stack: A stack is a basic data structure that can be logically thought as
    linear structure represented by a real physical stack or pile, a structure
    where insertion and deletion of items takes place at one end called top of
    the stack. The basic concept can be illustrated by thinking of your data set
    as a stack of plates or books where you can only take the top item off the
    stack in order to remove things from it. This structure is used all
    throughout programming.

    wiki: https://en.wikibooks.org/wiki/Data_Structures/Stacks_and_Queues
"""

class Stack:
    def __init__(self):
        self.items = list()

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"{self.items}"

    def push(self, item):
        """
        Add an element to the top of the stack
        Time Complexity: O(1)
        """
        self.items.append(item)

    def peek(self):
        """
        Return the top element. DO NOT remove it
        Time Complexity: O(1)
        """
        length = len(self.items)
        return self.items[length - 1] if length else None

    def pop(self):
        """
        Remove and return the top element. 
        Time Complexity: O(1)
        """
        try:
            return self.items.pop(len(self.items) - 1)
        except IndexError:
            raise IndexError("Pop from empty stack")
    
    def isEmpty(self):
        """
        Check if stack is empty
        """
        return not self.items
