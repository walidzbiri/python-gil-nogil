import concurrent.futures
import contextlib
from typing import Generator
import time

@contextlib.contextmanager
def time_it(what: str) -> Generator[None,None,None]:
    t0 = time.monotonic()
    try:
        yield
    finally:
        print(f"{what} took {time.monotonic()-t0}")


def do_work()-> int:
    with time_it("work"):
        x=0
        for _ in range(10_000_000):
            x+=1
        return x


def main(number_of_threads: int = 4) -> None:
    print(f"Running main function with {number_of_threads} threads ")
    with time_it("main"):
        with concurrent.futures.ThreadPoolExecutor(number_of_threads) as pool:
            futures=[pool.submit(do_work) for _ in range(20)]
            for future in concurrent.futures.as_completed(futures):
                print(f"got {future.result()}")


if __name__ == "__main__":
    main()


# Python 3.13 without GIL main took 1.4893241669997224 seconds
# Python 3.13 with GIL main took 5.016588582999248 seconds