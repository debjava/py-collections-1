import asyncio
import time


def fun_a():
    time.sleep(3)
    print("Completed Function A")
    return "a"

def fun_b():
    time.sleep(5)
    print("Completed Function B")
    return "b"

def fun_c():
    time.sleep(7)
    print("Completed Function C")
    return "c"

def fun_d():
    time.sleep(9)
    print("Completed Function D")
    return "d"

def fun_e():
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

async def async_concurrent_call():
    tasks = [
        async_fun_a(),
        async_fun_b(),
        async_fun_c(),
        async_fun_d(),
        async_fun_e()
    ]
    api_response_list = await asyncio.gather(*tasks)
    return api_response_list

if __name__ == "__main__":
    # all_responses = sequential_call()
    all_responses = asyncio.run(async_concurrent_call())
    for response in all_responses:
        print(f" Response from API: {response}")
