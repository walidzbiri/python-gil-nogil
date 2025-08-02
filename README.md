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

### .python.version file
This file helps you pin the python version used by the project. You can either use 3.13 or 3.13t (which is the interpreter that supports disabling GIL)

### How to run the project.
```console
foo@bar:~$ uv sync # to sync venv after changing python version
foo@bar:~$ uv run main.py # to run the project
```