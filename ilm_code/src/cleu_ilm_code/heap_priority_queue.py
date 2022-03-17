"""Priority Queue implementation in Python.

Heavily influenced by the explanation of Priority Queues here:
https://www.programiz.com/dsa/priority-queue
"""

from collections import namedtuple

QueueItem = namedtuple("queue_item", ["prio", "command", "orig_order"])

class ILMPrioQueue:
    """A simple priority queue class."""

    REQUIRED_KEYS = ["priority", "command"]

    def __init__(self):
        self.arr = []

    def _validate_entry(self, new_entry):
        """Validate a potential new entry to the queue.

        Args:
            new_entry(dict): A dictionary to use to create a queue entry.

        Returns:
            bool: Whether or not the entry is valid.
        """
        if not all(new_entry.get(key) for key in ["priority", "command"]):
            print(f"Entry is missing a required key ({self.REQUIRED_KEYS})")
            return False
        if not (isinstance(new_entry.get("priority"), int)):
            print(
                f"Priority must be an int not {type(new_entry.get('priority'))}"
            )
            return False
        if new_entry["priority"] > 10:
            print(
                f"Priority must be lower than 10 for command {new_entry.get('command')}"
            )
            return False
        return True

    def insert(self, new_entry):
        """Add an element to the queue.

        Args:
            new_entry(dict): A dictionary to use to create a queue entry.
        """
        if not self._validate_entry(new_entry):
            return
        size = len(self.arr)
        self.arr.append(
            QueueItem(
                prio=new_entry["priority"],
                command=new_entry["command"],
                orig_order=size
            )
        )
        if len(self.arr) > 1:
            size += 1
            for index in range((size // 2) - 1, -1, -1):
                self._heapify(size, index)

    def _compare_child_node(self, parent_index, child_index):
        """Compare 2 elements in our array, selecting the largest priority.

        There is a seconard comparison on the orig_order attribute which is
        used in the case of equal priorities, older elements being larger.

        Args:
            parent_index (int): The index of the parent.
            child_index (int): The index of the child.

        Returns:
            int: The index of the largest.
        """
        largest = parent_index
        if self.arr[parent_index].prio < self.arr[child_index].prio:
            largest = child_index
        elif self.arr[parent_index].prio == self.arr[child_index].prio:
            if self.arr[parent_index].orig_order > self.arr[child_index].orig_order:
                largest = child_index
        return largest

    def _heapify(self, size, index):
        """Re-arrange the tree to satisfy the conditions of a max heap.

        The array (self.arr) is manipulated as a binary tree such that each
        node is always greater than its child nodes. This is accomplished by
        examing the children of a node on the left and right and then swapping
        places with the child if it is larger.

        Args:
            size (int): The size of our array.
            index (int): The index of the element which we are examing the
                children of.
        """
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < size:
            largest = self._compare_child_node(index, left)

        if right < size:
            largest = self._compare_child_node(index, right)

        # Swap and continue heapifying if root is not largest
        if largest != index:
            self.arr[index], self.arr[largest] = self.arr[largest], self.arr[index]
            self._heapify(size, largest)

    def _get_index_in_arr(self, cmd):
        """Get the index of a command in the arry.

        Args:
            cmd (str): The command.

        Returns:
            int or None: The index of the command or None if not present.
        """
        to_remove_index = None
        for index in range(0, len(self.arr)):
            if cmd == self.arr[index].command:
                if to_remove_index:
                    if self.arr[index].orig_order > self.arr[to_remove_index].orig_order:
                        to_remove_index = index
                else:
                    to_remove_index = index
        return to_remove_index

    def remove(self, cmd):
        """Remove an element from our array and adjust queue accordingly.

        Args:
            cmd (str): The command.
        """
        size = len(self.arr)
        to_remove_index = self._get_index_in_arr(cmd)

        if to_remove_index is None:
            print(f"command '{cmd}' not found")
            return

        self.arr[to_remove_index], self.arr[size - 1] = self.arr[size - 1], self.arr[to_remove_index]

        del self.arr[size - 1]

        for index in range((len(self.arr) // 2) - 1, -1, -1):
            self._heapify(len(self.arr), index)
