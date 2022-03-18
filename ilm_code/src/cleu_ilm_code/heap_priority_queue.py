"""Priority Queue implementation in Python.

Heavily influenced by the explanation of Priority Queues here:
https://www.programiz.com/dsa/priority-queue
"""

from collections import namedtuple
import logging

QueueItem = namedtuple("queue_item", ["prio", "command", "orig_order"])

class ILMPrioQueue:
    """A simple priority queue class."""

    REQUIRED_KEYS = ["priority", "command"]

    def __init__(self, log_level="info"):
        """Initialize the class.

        Args:
            log_level (str): A logging level.
        """
        self._init_logging(log_level)
        self._arr = []

    def _init_logging(self, log_level):
        """Initialize the logger.

        Args:
            log_level (str): A logging level.
        """
        self._logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        if log_level == "info":
            self._logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
            self._logger.addHandler(ch)
        elif log_level == "error":
            self._logger.setLevel(logging.ERROR)
            ch.setLevel(logging.ERROR)
            self._logger.addHandler(ch)
        else:
            self._logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
            self._logger.addHandler(ch)
            self._logger.info(
                f"Log level {log_level} is unsupported, using INFO"
            )

    def _validate_entry(self, new_entry):
        """Validate a potential new entry to the queue.

        Args:
            new_entry(dict): A dictionary to use to create a queue entry.

        Returns:
            bool: Whether or not the entry is valid.
        """
        if not all(new_entry.get(key) for key in ["priority", "command"]):
            self._logger.info(
                f"Entry is missing a required key ({self.REQUIRED_KEYS})"
            )
            return False
        if not (isinstance(new_entry.get("priority"), int)):
            self._logger.info(
                (
                    f"Priority must be an int not"
                    f" {type(new_entry.get('priority'))}"
                )
            )
            return False
        if new_entry["priority"] > 10 and new_entry["priority"] < 0:
            self._logger.info(
                (
                    f"Priority must be lower than 10 and greater than or equal"
                    f" to 0 for command"
                    f" {new_entry.get('command')}"
                )
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
        size = len(self._arr)
        self._arr.append(
            QueueItem(
                prio=new_entry["priority"],
                command=new_entry["command"],
                orig_order=size
            )
        )
        if len(self._arr) > 1:
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
        if self._arr[parent_index].prio < self._arr[child_index].prio:
            largest = child_index
        elif self._arr[parent_index].prio == self._arr[child_index].prio:
            if self._arr[parent_index].orig_order > self._arr[child_index].orig_order:
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
            self._arr[index], self._arr[largest] = self._arr[largest], self._arr[index]
            self._heapify(size, largest)

    def _get_index_in_arr(self, cmd):
        """Get the index of a command in the array.

        Args:
            cmd (str): The command.

        Returns:
            int or None: The index of the command or None if not present.
        """
        to_remove_index = None
        for index in range(0, len(self._arr)):
            if cmd == self._arr[index].command:
                if to_remove_index:
                    if self._arr[index].orig_order > self._arr[to_remove_index].orig_order:
                        to_remove_index = index
                else:
                    to_remove_index = index
        return to_remove_index

    def remove(self, cmd):
        """Remove an element from our array and adjust queue accordingly.

        Args:
            cmd (str): The command.
        """
        size = len(self._arr)
        to_remove_index = self._get_index_in_arr(cmd)

        if to_remove_index is None:
            self._logger.info(f"command '{cmd}' not found")
            return

        self._arr[to_remove_index], self._arr[size - 1] = self._arr[size - 1], self._arr[to_remove_index]

        del self._arr[size - 1]

        for index in range((len(self._arr) // 2) - 1, -1, -1):
            self._heapify(len(self._arr), index)

    def pop(self):
        """Get the command at the top of the queue.

        Returns:
            str: The command with the highest priority.
        """
        if len(self._arr) <= 0:
            return None
        cmd = self._arr[0].command
        self.remove(cmd)
        return cmd
