import logging
import time
from math import sqrt

FORMAT = "[%(threadName)s][%(filename)s:%(lineno)s - %(funcName)10s()] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)


def fib():
    a = 2
    b = 1
    yield a
    while True:
        yield b
        a, b = b, a + b
        
        

class Task:
    next_id = 0
    
    def __init__(self, routine):
        self.id = Task.next_id
        self.routine = routine
        Task.next_id += 1


from collections import deque


class Scheduler: 

    def __init__(self):
        # Use a `deque` to pop and push tasks from both
        # end of the queue
        self.runnable_tasks = deque()
        # Use a `dict` to store the (task_id, task_result) pairs
        self.completed_task_result = {}
        self.failed_task_errors = {}

    def add(self, routine, name):
        # Wrap the routine with a `Task` and push the task to the queue
        task = Task(routine)
        self.runnable_tasks.append(task)
        self.name = name
        return task.id

    def run_to_completion(self):
        # While the queue is not empty, take the next task 
        # run it by calling `next`, try to catch the result
        # if the task is completed, otherwise push it back to
        # the end of the queue and pop out next task for
        # execution
        while len(self.runnable_tasks) != 0:
            task = self.runnable_tasks.popleft()
#             print(f"Running task {task.id}")
            try:
                # run task
                yielded = next(task.routine)
            # check result
            except StopIteration as stopped:
                print(f"----------------------\nTask {task.name} completed with result: {stopped.value}")
                self.completed_task_result[task.id] = stopped.value
            except Exception as e:
                print(f"Failed with exception: {e}")
            else: 
                assert yielded is None
                # print("now yielded")
                self.runnable_tasks.append(task)


def async_sleep(interval_secs):
    start = time.time()
    expiry = start + interval_secs
    while True:
        
        yield
        
        now = time.time()
        if now > expiry:
            
            break;


def async_is_prime(x):
    if x < 2:
        return False

    for i in range(2, int(sqrt(x))+1):
        if x % i == 0:
            return False
        
        # yield to avoid blocking on large numbers
        yield from async_sleep(0)
    
    return True

def async_print_matches(iterable, async_predicate):
    for item in iterable:
        # ` yield from` allows the predicate to make progress
        # and yield control
        matches = yield from async_predicate(item)
        if matches:
            print(f"Found: {item}")
            # Keep iterating instead of returning/interrupting  
            yield

  
def async_repetitive_message(msg, interval_secs):
    # Periodically print a message
    while True:
        print(msg)
        yield from async_sleep(interval_secs)
        

sched = Scheduler()
sched.add(async_repetitive_message('This is an async message', 2), 'Repetitive Message')
sched.add(async_print_matches(fib(), async_is_prime), 'Check Prime')
sched.run_to_completion()
