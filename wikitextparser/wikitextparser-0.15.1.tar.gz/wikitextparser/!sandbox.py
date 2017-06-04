import time
import ast
import inspect
from timeit import timeit


print(timeit('type(a).__name__', 'a=1; b=2; c=3', globals=globals()))
print(timeit('a.__class__.__name__', 'a=1; b=2; c=3', globals=globals()))
