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

import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor

from concurrent.futures import as_completed

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)


def do_sth(seconds: float) -> str:
    logger.info(f"Sleeping {seconds} second(s)...")
    
    time.sleep(seconds)
    
    msg = f"Done sleeping {seconds} second(s)."
    logger.info(msg)
    
    return msg


if __name__ == '__main__':
    logger.info("----------- Python Threading Demo --------------")
    
    start = time.perf_counter()

    with ThreadPoolExecutor() as executor:
#         future_1 = executor.submit(do_sth, 1)
#         future_2 = executor.submit(do_sth, 2)
        
        results =[executor.submit(do_sth, 10-i) for i in range(10)]
        
#         logger.info(f'f1 Result returned: {future_1.result()}')
#         logger.info(f'f2 Result returned: {future_2.result()}')

        for f in as_completed(results):
            logger.info('Result returned: {}'.format(f.result()))
        
    
    finish = time.perf_counter()
    
    logger.info(f"Finished in {round(finish-start, 2)} second(s)")
    
    
    
    
    