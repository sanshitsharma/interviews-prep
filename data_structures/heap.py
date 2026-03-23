"""
Heap is a special case of balanced binary tree data structure where the root-node key is compared
with its children and arranged accordingly. Depending on the criteria, a heap can be of two types:

1. Min Heap: The value of each node is less than or equal to the smaller of it's child nodes
2. Max heap: The value of each node is greater than or equal to the greater of it's child nodes

Because heaps are a variant of a balanced binary tree, a heap can be internally managed as an array.

Given an index "idx", the value of it's children and parent can be determined using the formulas:
    parent = (idx - 1)/2
    leftChild = 2*idx + 1
    rightChild = 2*idx + 2

https://www.tutorialspoint.com/data_structures_algorithms/heap_data_structure.htm
"""

from abc import ABC, abstractmethod

class Heap(ABC):
    def __init__(self):
        self.heap = list()

    def __repr__(self):
        return f"{self.heap}"

    def __len__(self):
        return len(self.heap)

    def getParentIndex(self, index):
        return int((index - 1)/2)

    def getLeftChildIndex(self, index):
        return int((2 * index) + 1)

    def getRightChildIndex(self, index):
        return int((2 * index) + 2)

    def hasParent(self, index):
        if self.getParentIndex(index) >= 0:
            return True

    def hasLeftChild(self, index):
        try:
            self.heap[self.getLeftChildIndex(index)]
            return True
        except IndexError:
            return False

    def hasRightChild(self, index):
        try:
            self.heap[self.getRightChildIndex(index)]
            return True
        except IndexError:
            return False

    def swap(self, indx1, indx2):
        self.heap[indx1], self.heap[indx2] = self.heap[indx2], self.heap[indx1]

    def peek(self):
        """
        Return the minimum element from the heap. DO NOT DELETE
        Time Complexity: O(1)
        """
        try:
            return self.heap[0]
        except IndexError:
            raise ValueError("Heap is empty")

    def poll(self):
        """
        Remove the minimum element from the heap.
        Time Complexity: O(log n)
        """
        try:
            elem = self.heap[0] # read the first element, we will return this 
        except IndexError:
            raise ValueError("Heap is empty")
        self.heap[0] = self.heap[len(self.heap) - 1] # Replace the root with the last element in the heap
        self.heap.pop() # Remove the last element
        self.heapifyDown()

        return elem

    def add(self, value):
        """
        Add a new element to the heap
        Time Complexity: O(log n)
        """
        self.heap.append(value)
        self.heapifyUp()

    @abstractmethod
    def pickChildIndex(self, currIdx, leftIdx, rightIdx):
        pass

    @abstractmethod
    def shouldSwap(self, currIdx, candidateIdx):
        pass

    def heapifyDown(self):
        """
        Working down from the root element at index 0, ensure heap properties
        """
        currIdx = 0
        while self.hasLeftChild(currIdx):
            # Compare with the children and swap if value at current index is greater than the smaller of the
            # two children
            swapCandidateIdx = self.pickChildIndex(currIdx, self.getLeftChildIndex(currIdx), self.getRightChildIndex(currIdx))

            if self.shouldSwap(currIdx, swapCandidateIdx):
                self.swap(currIdx, swapCandidateIdx)

            currIdx = swapCandidateIdx

            '''
            smallerChildIdx = self.getLeftChildIndex(currIdx)
            if self.hasRightChildIndex(currIdx) and self.heap[self.getRightChildIndex(currIdx)] < self.heap[self.getLeftChildIndex(currIdx)]:
                smallerChildIdx = self.getRightChildIndex(currIdx)

            if self.heap[currIdx] < self.heap[smallerChildIdx]:
                break
            else:
                self.swap(currIdx, smallerChildIdx)
            
            currIdx = smallerChildIdx
            '''

    def heapifyUp(self):
        """
        Working up from the last element at index length - 1, ensure heap properties
        """
        '''
        while self.hasParent(currIdx) and self.heap[currIdx] < self.heap[self.getParentIndex(currIdx)]:
            parentIdx = self.getParentIndex(currIdx)
            self.swap(currIdx, parentIdx)
            currIdx = parentIdx
        '''
        currIdx = len(self.heap) - 1
        while self.hasParent(currIdx):
            parentIdx = self.getParentIndex(currIdx)
            if not self.shouldSwap(parentIdx, currIdx):
                break
            else:
                self.swap(currIdx, parentIdx)
                currIdx = parentIdx

class MinHeap(Heap):
    def pickChildIndex(self, currIdx, leftIndex, rightIndex):
        smallerChildIdx = leftIndex
        if self.hasRightChild(currIdx) and self.heap[rightIndex] < self.heap[leftIndex]:
            smallerChildIdx = rightIndex

        return smallerChildIdx

    def shouldSwap(self, currIdx, candidateIdx):
        return self.heap[currIdx] > self.heap[candidateIdx]

class MaxHeap(Heap):
    def pickChildIndex(self, currIdx, leftIndex, rightIndex):
        largerChildIndex = leftIndex
        if self.hasRightChild(currIdx) and self.heap[rightIndex] > self.heap[leftIndex]:
            largerChildIndex = rightIndex

        return largerChildIndex

    def shouldSwap(self, currIdx, candidateIdx):
        return self.heap[currIdx] < self.heap[candidateIdx]
