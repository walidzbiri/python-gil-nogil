# Python GIL VS No GIL

In the realm of Python development, achieving parallelism and harnessing the full power of modern multi-core processors is challenging.

Traditionally constrained by the Global Interpreter Lock (GIL), multi-threading was not useful for true parallelism in Python, hence developers turned into multi-processing. 

***Now this is all changing with upcoming developments.***

It is possible to disable the GIL on the C-Python interpreters since 3.13.  

> [!WARNING]  
> Don't use this type of interpreters on production. It is still expiremental !

## How to setup the project locally

### UV to manage python interpreter versions
Check uv documentation: https://docs.astral.sh/uv/getting-started/installation/

### How to run the project.
```console
foo@bar:~$ uv run main.py # to run the project with GIL
foo@bar:~$ PYTHON_GIL=0 uv run main.py # to run the project without GIL
```

## Analyzing benchmark results
#### With GIL
| Scenario       | Threads | Speedup |
|----------------|---------|---------|
| Single Thread  | 1       | 1.00x   |
| 2 Threads      | 2       | 1.00x   |
| 4 Threads      | 4       | 1.04x   |
| 8 Threads      | 8       | 1.00x   |

We all know that the CPython GIL blocks the interpreter from running multiple threads in parallel. It was designed to protect python developers by preventing race conditions and deadlocks. Simplifies memory management (garbage collector) and makes it easier to write thread-safe code.

So when running many threads againt a list of tasks it could be slower than running one thread. Because of the overhead of context switching between all threads since it is running them concurrently.


#### Without GIL
| Scenario       | Threads | Speedup |
|----------------|---------|---------|
| Single Thread  | 1       | 1.00x   |
| 2 Threads      | 2       | 1.94x   |
| 4 Threads      | 4       | 2.95x   |
| 8 Threads      | 8       | 3.00x   |

Disabling the GIL allows the interpreter to parallelize threads execution which will absolutely speed-up tasks execution. 

Removing the GIL could have potential issues like:
- It may break existing python code:
    - Thread safety.
    - Memory management.
    - Single threaded performance may decrease.
- It may break libraries relying on it:
    - Since it has impact on the C API, it will break libraries like numpy ...

## Read More and watch later
- https://peps.python.org/pep-0703/
- https://www.youtube.com/watch?v=HdTtJKevxfQ
- https://www.youtube.com/watch?v=6g79qGQo2-Q
