import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import aiohttp
import requests
from requests import Response

def make_api_call(url: str) -> Any:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
    response_json: Any = response.json()

    return response_json

def get_response_from_url(url: str):
    response = requests.get(url)
    response_json: Any = response.json()
    return url, response.status_code, response_json

def get_object_urls():
    object_urls_list: list[str] = []
    for i in range(1,14):
        call_url = f"https://api.restful-api.dev/objects/{i}"
        object_urls_list.append(call_url)
    return object_urls_list

def get_all_countries() -> dict[str,str]:
    country_id_name_dict: dict[str, str] = dict()
    all_country_url = f"https://apihero-api.quixtools.com/api/v1/location/getCountriesAll"
    response = requests.get(all_country_url)
    if response.status_code != 200:
        print(f"Request failed. Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return country_id_name_dict
    response_json: Response = response.json()
    # print(f"Response: {response_json}")
    for country in response_json.get("data", []):
        country_id = country.get("countryId")
        country_name = country.get("countryName")
        # print(f"Country Id: {country_id}, Country Name: {country_name}")
        if country_id is not None and country_name is not None:
            country_id_name_dict[country_id] = country_name

    return country_id_name_dict

def get_all_urls_by_country_id() -> list[str]:
    all_urls: list[str] = list()
    country_dict: dict[str, str] = get_all_countries()
    for country_id, value in country_dict.items():
        url_by_country_id = f"https://apihero-api.quixtools.com/api/v1/location/getCountry/{country_id}"
        all_urls.append(url_by_country_id)

    return all_urls


def get_all_urls():
    all_urls: list[str] = list()
    object_urls: list[str] = get_object_urls()
    country_urls: list[str] = get_all_urls_by_country_id()
    all_urls.extend(object_urls)
    all_urls.extend(country_urls)

    return all_urls

def make_sequential_api_call():
    response_list: list[Any] = list()
    urls_list: list[str] = get_all_urls()
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
    urls_list: list[str] = get_all_urls()

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
    urls_list: list[str] = get_all_urls()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls_list:
            task = make_api_call_async(session, url)
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
    # make_parallel_api_call() # 85.766622 seconds
    asyncio.run(make_parallel_call_asyncio()) # 4.787933 seconds

    end_time_s = time.perf_counter()
    print(f"Time taken: {end_time_s - start_time_s:.6f} seconds") # Time taken: 240.905411 seconds



