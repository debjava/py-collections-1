import asyncio
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List

import aiohttp
import requests

def make_api_call(url: str) -> Any:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
    response_json: Any = response.json()

    return response_json

def get_response_from_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        response_json: Any = response.json()
        return url, response.status_code, response_json
    except (requests.exceptions.ConnectionError, 
            requests.exceptions.RequestException, 
            requests.exceptions.Timeout) as e:
        print(f"Error fetching {url}: {str(e)}")
        return url, -1, {"error": str(e)}

def get_response_from_url11(url: str):
    try:
        response = requests.get(url, timeout=10)
        response_json: Any = response.json()
        return url, response.status_code, response_json
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {str(e)}")
        return url, -1, {"error": str(e)}


def get_300_api_urls():
    all_urls: list[str] = list()
    for i in range(1,301):
        url = f"https://jsonplaceholder.typicode.com/comments/{i}"
        all_urls.append(url)
    return all_urls

def make_sequential_api_call():
    response_list: list[Any] = list()
    # urls_list: list[str] = get_all_urls()
    urls_list: list[str] = get_300_api_urls()
    for url in urls_list:
        # json_response = make_api_call(url)
        response_details: Any = get_response_from_url(url)
        response_list.append(response_details)

    # Iterate the response_list and print the details
    for response_details in response_list:
        url, status, response_json = response_details
        print(f"URL: {url}")
        print(f"Status: {status}")
        print(f"JSON: {response_json}")
        print("-" * 40)


    return response_list

def make_parallel_api_call():
    results = []
    url_to_status: dict[str, dict[str, Any]] = {}
    urls_list: list[str] = get_300_api_urls()

    # Total Maximum Threads: 4
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures_result = [] # It is list of future
        for url in urls_list:
            future = executor.submit(get_response_from_url, url)
            futures_result.append(future)

    # Collect results as they finish
    for future in as_completed(futures_result):
        url, status, response_json = future.result()
        url_to_status[url] = {"status": status, "json": response_json}
        print(f"Completed API Call URL: {url}")
        print(f"Response Status: {status}")
        results.append((url, status, response_json))

    return url_to_status

def make_parallel_api_call11():
    results = []
    url_to_status: dict[str, dict[str, Any]] = {}
    urls_list: list[str] = get_300_api_urls()

    total_threads: int = multiprocessing.cpu_count() * 4 # Total No of Core 8, total threads 8 * 4 = 32
    max_worker_count: int = min(len(urls_list), total_threads) # Total threads: 32
    executor = ThreadPoolExecutor(max_workers=max_worker_count)
    
    try:
        futures_result = [] # It is list of future
        for url in urls_list:
            future = executor.submit(get_response_from_url, url)
            futures_result.append(future)

        # Collect results as they finish
        for future in as_completed(futures_result):
            url, status, response_json = future.result()
            url_to_status[url] = {"status": status, "json": response_json}
            print(f"Completed API Call URL: {url}")
            print(f"Response Status: {status}")
            results.append((url, status, response_json))
            
    finally:
        executor.shutdown()
    
    return url_to_status

async def make_api_call_async(session: aiohttp.ClientSession, url: str) -> tuple[str, int, Any]:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Request failed. Status code: {response.status}")
                response_text = await response.text()
                print(f"Response text: {response_text}")
                return url, response.status, {}
            
            response_json = await response.json()
            return url, response.status, response_json
    except Exception as e:
        print(f"Error making request to {url}: {e}")
        return url, 0, {}

async def make_parallel_call_asyncio():
    urls_list: list[str] = get_300_api_urls()
    print(f"Total URLs: {len(urls_list)}")
    
    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task[tuple[str, int, Any]]] = list()
        for url in urls_list:
            task = asyncio.create_task(make_api_call_async(session, url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        url_to_status: dict[str, dict[str, Any]] = {}
        for result in results:
            if isinstance(result, Exception):
                print(f"Task failed with exception: {result}")
                continue
            
            url, status, response_json = result
            url_to_status[url] = {"status": status, "json": response_json}
            print(f"Completed API Call URL: {url}")
            print(f"Response Status: {status}")
        
        return url_to_status
    

if __name__ == "__main__":
    # urls_list: list[str] = get_all_urls() # Total 208 urls

    start_time_s = time.perf_counter()

    # make_sequential_api_call() # 264 seconds
    # make_parallel_api_call() # 83 - 111 seconds
    # make_parallel_api_call11() # 58 seconds
    asyncio.run(make_parallel_call_asyncio()) # 3.700589 seconds, 4 seconds

    end_time_s = time.perf_counter()
    print(f"Time taken: {end_time_s - start_time_s:.6f} seconds") # Time taken: 240.905411 seconds
    # print(f"multiprocessing.cpu_count()------>{multiprocessing.cpu_count()}") # 8
    # max_worker_count: int = multiprocessing.cpu_count() * 4
    # print(f"Total worker count: {max_worker_count}")



