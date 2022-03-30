import unittest

import sys
sys.path.append("/home/chris/dev/ilm_code/src/cleu_ilm_code")

from heap_priority_queue import ILMPrioQueue, QueueItem


class TestILMPrioQueue(unittest.TestCase):
    """Various tests for ILMPrioQueue."""

    def test_validate_entry(self):
        """Test the validate_entry func."""
        my_queue = ILMPrioQueue(log_level="error")
        bad_keys = my_queue._validate_entry(
            {"priority": 3, "nothing": "my_cmd"}
        )
        bad_prio_type = my_queue._validate_entry(
            {"priority": 1.1, "command": "my_cmd"}
        )
        bad_prio_val = my_queue._validate_entry(
            {"priority": 11, "command": "my_cmd"}
        )
        self.assertFalse(all([bad_keys, bad_prio_type, bad_prio_val]))

        good_keys = my_queue._validate_entry(
            {"priority": 3, "command": "my_cmd"}
        )
        self.assertTrue(all([good_keys]))

    def test_insert(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "only_cmd"})
        self.assertEqual(len(my_queue._arr), 1)

    def test_compare_child_node(self):
        my_queue = ILMPrioQueue(log_level="error")
        one = QueueItem(
            prio=1,
            command="one_cmd",
            orig_order=0
        )
        two = QueueItem(
            prio=2,
            command="two_cmd",
            orig_order=0
        )
        my_queue._arr = [one, two]
        self.assertEqual(my_queue._compare_child_node(0, 1), 1)

    def test_heapify(self):
        my_queue = ILMPrioQueue(log_level="error")
        one = QueueItem(
            prio=1,
            command="one_cmd",
            orig_order=0
        )
        two = QueueItem(
            prio=2,
            command="two_cmd",
            orig_order=0
        )
        three = QueueItem(
            prio=10,
            command="ten_cmd",
            orig_order=0
        )
        my_queue._arr = [one, two, three]
        for index in range((len(my_queue._arr) // 2) - 1, -1, -1):
            my_queue._heapify(len(my_queue._arr) + 1, index)
        self.assertEqual(my_queue._arr[0].command, "ten_cmd")

    def test_get_index_in_arr(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        my_queue.insert({"priority": 7, "command": "second_cmd"})
        my_queue.insert({"priority": 1, "command": "third_cmd"})
        my_queue.insert({"priority": 3, "command": "third_cmd"})
        self.assertEqual(my_queue._get_index_in_arr("third_cmd"), 3)

    def test_remove(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        my_queue.insert({"priority": 7, "command": "second_cmd"})
        my_queue.insert({"priority": 1, "command": "third_cmd"})
        my_queue.remove("first_cmd")
        self.assertEqual(len(my_queue._arr), 2)

    def test_pop(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        self.assertEqual(my_queue.pop(), "first_cmd")

    def test_add_dup(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        self.assertEqual(my_queue._arr[0].orig_order, 0)

    def test_remove_nonexistant(self):
        my_queue = ILMPrioQueue(log_level="error")
        my_queue.insert({"priority": 10, "command": "first_cmd"})
        my_queue.remove("made_up_cmd")
        self.assertEqual(len(my_queue._arr), 1)
