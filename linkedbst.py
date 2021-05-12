"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time
from math import log2, ceil
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            if item < node.data:
                return recurse(node.left)
            return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() <= ceil(log2(self._size + 1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        items = list(self.inorder())
        list_in_range = []

        for item in items:
            if item in range(low, high+1):
                list_in_range.append(item)

        return list_in_range

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        initial = list(self.inorder())
        self.clear()

        def recurse(lst):
            """Helper function for rebalance"""
            if lst:
                mid_idx = len(lst)//2
                self.add(lst[mid_idx])

                recurse(lst[:mid_idx])
                recurse(lst[mid_idx+1:])

        recurse(initial)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root

        while True:
            if item >= root.data:
                if root.right is not None:
                    root = root.right
                else:
                    return None
            else:
                old_root = root.data
                break

        while True:
            if item > root.data:
                return old_root

            if root.left is not None:
                old_root = root.data
                root = root.left
            else:
                return root.data

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        root = self._root
        predecessors = []

        while True:
            if item < root.data:
                if root.left is not None:
                    root = root.left
                else:
                    break

            elif item > root.data:
                predecessors.append(root.data)
                if root.right is not None:
                    root = root.right
                else:
                    break

            elif item == root.data:
                if root.left is not None:
                    root = root.left
                else:
                    break

            else:
                break

        if len(predecessors) > 0:
            return max(predecessors)
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # File reader
        words_list = []

        with open(path, mode='r', encoding='utf-8') as words:
            for word in words:
                words_list.append(word.strip("\n"))

        # Random words (900) instead of 10 000
        number = 900
        sample = random.sample(words_list, number)
        sample.sort()

        # Trees
        sorted_words_tree = LinkedBST(sample)
        random.shuffle(sample)
        random_words_tree = LinkedBST(sample)
        LinkedBST(sample).rebalance()
        balanced_words_tree = LinkedBST(sample)

        # Sorted list case
        start = time.time()
        for i in range(10000):
            _ = words_list.index(sample[random.randint(0, len(sample)-1)])
        end = time.time()
        sorted_list_time = end - start

        # Sorted BST case
        start = time.time()
        for i in range(10000):
            _ = sorted_words_tree.find(
                sample[random.randint(0, len(sample)-1)])
        end = time.time()
        sorted_bst_time = end - start

        # Random BST case
        start = time.time()
        for i in range(10000):
            _ = random_words_tree.find(
                sample[random.randint(0, len(sample)-1)])
        end = time.time()
        random_bst_time = end - start

        # Balanced BST case
        start = time.time()
        for i in range(10000):
            _ = balanced_words_tree.find(
                sample[random.randint(0, len(sample)-1)])
        end = time.time()
        balanced_bst_time = end - start

        # Output
        string = f"Sorted List: {sorted_list_time}\nSorted BST: {sorted_bst_time}\nRandom BST: {random_bst_time}\nBalanced BST: {balanced_bst_time}\n"
        return string


if __name__ == '__main__':
    T = LinkedBST()
    print(T.demo_bst("Task1/words.txt"))
