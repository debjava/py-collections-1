import asyncio
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Any


def fun_a(param: str=None):
    print(f"Param: {param}")
    time.sleep(3)
    print("Completed Function A")
    return "a"

def fun_b(param: str=None):
    print(f"Param: {param}")
    time.sleep(5)
    print("Completed Function B")
    return "b"

def fun_c(param: str=None):
    print(f"Param: {param}")
    time.sleep(7)
    print("Completed Function C")
    return "c"

def fun_d(param: str=None):
    print(f"Param: {param}")
    time.sleep(9)
    print("Completed Function D")
    return "d"

def fun_e(param: str=None):
    print(f"Param: {param}")
    time.sleep(11)
    print("Completed Function E")
    return "e"



async def async_fun_a():
    return await asyncio.to_thread(fun_a)

async def async_fun_b():
    return await asyncio.to_thread(fun_b)

async def async_fun_c():
    return await asyncio.to_thread(fun_c)

async def async_fun_d():
    return await asyncio.to_thread(fun_d)

async def async_fun_e():
    return await asyncio.to_thread(fun_e)

def sequential_call():
    api_response_list: list[str] = list()
    api_response_list.append(fun_a())
    api_response_list.append(fun_b())
    api_response_list.append(fun_c())
    api_response_list.append(fun_d())
    api_response_list.append(fun_e())
    return api_response_list

def make_parallel_call():
    max_thread_count = 5
    with ThreadPoolExecutor(max_workers=max_thread_count) as executor:
        futures = [
            executor.submit(fun_a, "param1"),
            executor.submit(fun_b, "param1"),
            executor.submit(fun_c, "param1"),
            executor.submit(fun_d, "param1"),
            executor.submit(fun_e, "param1")
        ]
        api_response_list: list[str] = list()
        for future in futures:
            api_response_list.append(future.result())
        return api_response_list

def make_parallel_call11():
    api_response_list: list[Any] = list()
    max_thread_count = 5
    function_list = [fun_a, fun_b, fun_c, fun_d, fun_e]
    future_list: list[Future] = list()
    with ThreadPoolExecutor(max_workers=max_thread_count) as executor:
        for func in function_list:
            future = executor.submit(func, "param1")
            future_list.append(future)

        for future in future_list:
            result = future.result()
            api_response_list.append(result)
        return api_response_list

async def async_concurrent_call():
    tasks: List[asyncio.Task[str]] = [
        asyncio.create_task(async_fun_a()),
        asyncio.create_task(async_fun_b()),
        asyncio.create_task(async_fun_c()),
        asyncio.create_task(async_fun_d()),
        asyncio.create_task(async_fun_e())
    ]
    api_response_list = await asyncio.gather(*tasks)
    return api_response_list

async def async_parallel_call():
    param1: str = "param1"
    tasks: List[asyncio.Task[str]] = [
        asyncio.create_task(asyncio.to_thread(fun_a,param1)),
        asyncio.create_task(asyncio.to_thread(fun_b, param1)),
        asyncio.create_task(asyncio.to_thread(fun_c, param1)),
        asyncio.create_task(asyncio.to_thread(fun_d, param1)),
        asyncio.create_task(asyncio.to_thread(fun_e, param1))
    ]
    api_response_list = await asyncio.gather(*tasks)
    return api_response_list

if __name__ == "__main__":
    start_time_s = time.perf_counter()
    # all_responses = sequential_call() # 35 seconds
    # all_responses = make_parallel_call() # 11 seconds
    # all_responses = make_parallel_call11() # 11 seconds
    # all_responses = asyncio.run(async_concurrent_call()) # 11 seconds
    all_responses = asyncio.run(async_parallel_call()) # 11 seconds, also working fine
    for response in all_responses:
        print(f" Response from API: {response}")

    end_time_s = time.perf_counter()
    print(f"Time taken: {end_time_s - start_time_s:.6f} seconds")  # Time taken: 240.905411 seconds

