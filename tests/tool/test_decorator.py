import time
from WeTest.tool.decorator import timeit


def test_decorator():
    
    @timeit
    def add(x, y):
        time.sleep(2)
        
        return x + y
    
    add(1, 2)