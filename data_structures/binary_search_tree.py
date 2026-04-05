"""
A Binary Search Tree (BST) is a special type of binary tree that maintains
its elements in a sorted order. It is a non-linear, hierarchical 
data structure, where each node can have at most two children,
and elements are organized in a parent-child relationship.

For every node in the BST:
- All nodes in its left subtree have values less than the node’s value.
- All nodes in its right subtree have values greater than the node’s value.

This property ensures that each comparison allows the operation 
to skip about half of the remaining tree, making BST operations
much faster than linear structures like arrays or linked lists.

https://www.geeksforgeeks.org/dsa/introduction-to-binary-search-tree/
"""

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"value: {self.value}, left: {self.left}, right: {self.right}"

class BST:
    def __init__(self):
        self.root = None

    def __repr__(self):
        return f"{self.inorder()}"

    def insert(self, value):
        """
        Insert a new node into the BST
        """
        if not self.root:
            self.root = TreeNode(value)
            return

        self._insert(self.root, value)

    def _insert(self, root, value):
        if not root:
            root = TreeNode(value)
        elif value <= root.value:
            # Go left
            root.left = self._insert(root.left, value)
        else:
            # Go right
            root.right = self._insert(root.right, value)

        return root

    def search(self, value):
        """
        Check if a value exists in the BST
        """
        return self._search(self.root, value)

    def _search(self, root, value):
        if not root:
            return False
        
        if root.value == value:
            return True

        if value <= root.value:
            # Go left
            return self._search(root.left, value)
        else:
            # Go right
            return self._search(root.right, value)

    def inorder(self):
        """
        Return the inorder (left, root, right) traversal of the tree 
        """
        elems = list()
        self._inorder(self.root, elems)
        return elems

    def _inorder(self, root, elems):
        if not root:
            return

        self._inorder(root.left, elems)
        elems.append(root.value)
        self._inorder(root.right, elems)

    def preorder(self):
        """
        Return the preorder (root, left, right) traversal of the tree
        """
        elems = list()
        self._preorder(self.root, elems)
        return elems

    def _preorder(self, root, elems):
        if not root:
            return

        elems.append(root.value)
        self._preorder(root.left, elems)
        self._preorder(root.right, elems)

    def postorder(self):
        """
        Return the postorder (left, right, root) traversal of the tree
        """
        elems = list()
        self._postorder(self.root, elems)
        return elems

    def _postorder(self, root, elems):
        if not root:
            return

        self._postorder(root.left, elems)
        self._postorder(root.right, elems)
        elems.append(root.value)

    def levelorder(self):
        if not self.root:
            return []

        q = list()
        elems = list()
        q.append(self.root)
        self._levelorder(q, elems)
        return elems

    def _levelorder(self, q, elems):
        while q:
            curr = q.pop(0)
            elems.append(curr.value)
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

    def delete(self, value):
        """
        Deletes the node with "value" from the BST. Deletion steps
        1. If a node with target value doesn't exist in the tree, then throw ValueError
        2. Else: first find the target node (TN) and it's parent node (PN)
            a. If TN is a leaf node, then just set the PN pointer to TN to null
            b. If TN has one child, then set the pointer from PN to TN's child
            c. If TN has two child nodes, then swap the value of TN with its inorder successor
               and make the new node as TN and continue until TN we hit one of the 2 former
               cases
        """
        parent = None
        curr = self.root
        curr, parent = self._search_for_delete(curr, parent, value)
        if not curr:
            # We traversed the entire tree but couldn't find a node with target value
            raise ValueError(f"Tree doesn't contain a node with value {value}")
        if not parent:
            print(f"Found node {curr.value} at root")
        else:
            print(f"Found node {curr.value} with parent {parent.value}")

        self._delete(curr, parent)

    def _delete(self, curr, parent):
        # By the time we get here, we already know that the node exists and it needs to be
        # deleted

        if not curr.left and not curr.right:
            # Target node is a leaf node
            self._stitch(curr, parent, None)
        elif curr.left and not curr.right:
            # Target node has a left child 
            self._stitch(curr, parent, curr.left)
        elif not curr.left and curr.right:
            # Target node has a right child
            self._stitch(curr, parent, curr.right)
        else:
            # Target node has two children
            successor, succ_parent = self._inorder_successor(curr, parent)
            curr.value, successor.value = successor.value, curr.value # swap
            self._delete(successor, succ_parent) 

        return

    def _stitch(self, curr, parent, target):
        if not parent:
            self.root = target
            return

        if parent.left == curr:
            parent.left = target
        else:
            parent.right = target

    def _inorder_successor(self, curr, parent):
        parent = curr
        curr = curr.right

        while curr.left:
            parent = curr
            curr = curr.left

        return curr, parent

    def _search_for_delete(self, curr, parent, value):
        if not curr or curr.value == value:
            return curr, parent

        parent = curr
        if value < curr.value: 
            curr = curr.left
        else:
            curr = curr.right
        return self._search_for_delete(curr, parent, value)
