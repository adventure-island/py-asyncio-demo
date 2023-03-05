'''
Created on Oct 31, 2020

CPU-BOUND: Computation-intensive tasks, can get worse when using threading
    because added overhead cost involved when creating/destroying threads
IO-BOUND: IO-blocking tasks, lots of waiting around INPUT and OUTPUT ops

Threading: 
 - NOT running code at the same time
 - An 'illusion' of parallelism
 
@author: JJ
'''

import os
import logging
import time
import threading

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)


def do_sth(seconds: float, id) -> None:
    logger.info(f"Thread ID: {id}, Sleeping {seconds} second...")
    time.sleep(seconds)
    logger.info(f"Thread ID: {id}, Done sleeping...")


if __name__ == '__main__':
    logger.info("----------- Python Threading Demo --------------")
    
    t1 = threading.Thread(target=do_sth)
    t2 = threading.Thread(target=do_sth)
    
    start = time.perf_counter()
    
#     do_sth()
#     do_sth()

#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()

    ts = []
    for i in range(10):
        t = threading.Thread(target=do_sth, args=[1.5, i])
        t.start()
        ts.append(t)
        
    for t in ts:
        t.join()
    
    finish = time.perf_counter()
    
    logger.info(f"Finished in {round(finish-start, 2)} second(s)")
    
    
    
    
    