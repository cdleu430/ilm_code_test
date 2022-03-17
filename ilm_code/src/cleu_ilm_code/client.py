"""

"""

import sys
sys.path.append("/home/chris/dev/ilm_code/src/cleu_ilm_code")

from heap_priority_queue import ILMPrioQueue

my_queue = ILMPrioQueue()

my_queue.insert({"priority": 4, "command": "run_sixth_cmd"})
my_queue.insert({"priority": 3, "command": "run_seventh_cmd"})
my_queue.insert({"priority": 8, "command": "run_third_cmd"})
my_queue.insert({"priority": 5, "command": "run_fifth_cmd"})
my_queue.insert({"priority": 7, "command": "run_fourth_cmd"})
my_queue.insert({"priority": 2, "command": "run_eigth_cmd"})
my_queue.insert({"priority": 10, "command": "run_first_cmd"})
my_queue.insert({"priority": 11, "command": "run_first_cmd"})


my_queue.remove("run_first_cmd")
my_queue.remove("run_sixth_cmd")

my_queue.insert({"priority": 9, "command": ""})


my_queue.insert({"priority": 5, "command": "run_fifth_cmd"})
my_queue.remove("run_fifth_cmd")



for i in my_queue.arr:
    print(i)
print("*"*5)
print(my_queue.arr[0])
