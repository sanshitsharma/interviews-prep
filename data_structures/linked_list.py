"""
    A linked list is a linear collection of data elements, called nodes, each
    pointing to the next node by means of a pointer. It is a data structure
    consisting of a group of nodes which together represent a sequence.

    wiki: https://en.wikipedia.org/wiki/Linked_list

"""

class ListNode():
    def __init__(self, value):
        self.value = value 
        self.next = None

    def __repr__(self):
        return f"value: {self.value}, next: {self.next}"

class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        curr = self.head
        ll = ""
        while curr:
            ll += f"{curr.value}"
            if curr.next:
                ll += " -> "
            curr = curr.next
        return ll
    
    def insert(self, value):
        """
        Add a new item to the end of the linked list
        Time Complexity: O(n)
        """
        newNode = ListNode(value)

        if not self.head:
            self.head = newNode 
            return

        # Go to the end of the list and add
        curr = self.head
        while curr.next:
            curr = curr.next
        
        curr.next = newNode

    def contains(self, value):
        """
        Checks if a value exists in the linked list
        Time Complexity: O(n)
        """
        curr = self.head
        while curr:
            if curr.value == value:
                return True
            curr = curr.next

        return False

    def delete(self, value):
        """
        Deletes the node with "value" from linked list if it exists
        Time Complexity: O(n)
        """
        if not self.head:
            raise ValueError(f"Value {value} not found in linked list")

        prev = None
        curr = self.head

        while curr:
            if curr.value == value:
                # If value found, Remove this node
                if not prev:
                    self.head = curr.next
                else:
                    prev.next = curr.next
                return
            
            prev = curr
            curr = curr.next

        # If we got here, it means we traversed the entire list and value was not found
        raise ValueError(f"Value {value} not found in linked list")
