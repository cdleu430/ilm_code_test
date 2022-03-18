import sys
sys.path.append("/home/chris/dev/ilm_code/src/cleu_ilm_code")

from heap_priority_queue import ILMPrioQueue, QueueItem


def test_validate_entry():
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
    try:
        assert not all([bad_keys, bad_prio_type, bad_prio_val])
    except AssertionError:
        print("[FAIL] test_validate_entry has failed.")
        return
    print("[PASS] test_validate_entry has passed")


def test_insert():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "only_cmd"})
    try:
        assert len(my_queue._arr) == 1
    except AssertionError:
        print("[FAIL] test_insert has failed.")
        return
    print("[PASS] test_insert has passed")


def test_compare_child_node():
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
    try:
        assert my_queue._compare_child_node(0, 1) == 1
    except AssertionError:
        print("[FAIL] test_compare_child_node has failed.")
        return
    print("[PASS] test_compare_child_node has passed")


def test_heapify():
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
    try:
        assert my_queue._arr[0].command == "ten_cmd"
    except AssertionError:
        print("[FAIL] test_heapify failed")
        return
    print("[PASS] test_heapify has passed")


def test_get_index_in_arr():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    my_queue.insert({"priority": 7, "command": "second_cmd"})
    my_queue.insert({"priority": 1, "command": "third_cmd"})
    my_queue.insert({"priority": 3, "command": "third_cmd"})
    try:
        assert my_queue._get_index_in_arr("third_cmd") == 3
    except AssertionError:
        print("[FAIL] test_get_index_in_arr has failed")
        return
    print("[PASS] test_get_index_in_arr has passed")


def test_remove():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    my_queue.insert({"priority": 7, "command": "second_cmd"})
    my_queue.insert({"priority": 1, "command": "third_cmd"})
    my_queue.remove("first_cmd")
    try:
        assert len(my_queue._arr) == 2
    except AssertionError:
        print("[FAIL] test_remove has failed")
        return
    print("[PASS] test_remove has passed")


def test_pop():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    try:
        assert my_queue.pop() == "first_cmd"
    except AssertionError:
        print("[FAIL] test_pop has failed")
        return
    print("[PASS] test_pop has passed")


def test_add_dup():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    try:
        assert my_queue._arr[0].orig_order == 0
    except AssertionError:
        print("[FAIL] test_add_dup has failed")
        return
    print("[PASS] test_add_dup has passed")


def test_remove_nonexistant():
    my_queue = ILMPrioQueue(log_level="error")
    my_queue.insert({"priority": 10, "command": "first_cmd"})
    my_queue.remove("made_up_cmd")
    try:
        assert len(my_queue._arr) == 1
    except AssertionError:
        print("[FAIL] test_remove_nonexistant has failed")
        return
    print("[PASS] test_remove_nonexistant has passed")


def main():
    print("Running tests...")
    test_validate_entry()
    test_insert()
    test_compare_child_node()
    test_heapify()
    test_get_index_in_arr()
    test_remove()
    test_pop()
    test_add_dup()
    test_remove_nonexistant()


if __name__ == "__main__":
    main()
