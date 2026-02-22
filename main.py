from collections import namedtuple
from typing import Any


def tuple_ops1():
    fruits_tuple1 : tuple[str] = ("apple", "banana", "cherry")
    for fruit in fruits_tuple1:
        print(f"Value: {fruit}")

    print("Total Length of tuple: ", len(fruits_tuple1))
    # With enumeration
    for index, fruit in enumerate(fruits_tuple1):
        print(f"Index: {index}, Value: {fruit}")

    my_mixed_tuple: tuple[str, int, float, bool, None] = ("hello", 1, 2.5, True, None)
    print(my_mixed_tuple)  # Output: ('hello', 1, 2.5, True, None)

    my_tuple: tuple[Any] = ("hello", 1, 2.5, True, None)
    print(my_tuple)  # Output: ('hello', 1, 2.5, True, None)

    my_tuple2: tuple[object] = ("hello", 1, 2.5, True, None)
    print(my_tuple2)  # Output: ('hello', 1, 2.5, True, None)

    # Convert to list, add a value and then convert to tuple
    furit_list: list[str] = list(fruits_tuple1)
    furit_list.append("orange")
    fruits_tuple2: tuple[str] = tuple(furit_list)
    print(fruits_tuple2)  # Output: ('apple', 'banana', 'cherry', 'orange')

    # Accessing tuple elements by index
    for i in range(len(fruits_tuple2)):
        print(f"{i} in fruits_tuple: {fruits_tuple2[i]}")

    # concatenate two tuples
    fruits_tuple3: tuple[str] = fruits_tuple1 + fruits_tuple2
    print(fruits_tuple3)

    # Find the number of appearance of a value in tuple
    tup1 = (10, 20, 45, 10, 30, 10, 55)
    print("Tup1:", tup1)
    c = tup1.count(10)
    print("count of 10:", c)


def usage_of_named_tuple():
    Point = namedtuple('Point', ['x', 'y'])
    # Create an instance
    p = Point(10, 20)
    # Access fields by indexing
    print("Point-1", p[0])
    print("Point-2", p[1])

    # Create a named tuple to represent a book
    Book = namedtuple('Book', ['title', 'author', 'year'])
    book = Book(title='To Kill a Mockingbird', author='Harper Lee', year=1960)
    print(book.title)  # Output: To Kill a Mockingbird
    print(book.author)  # Output: Harper Lee
    print(book.year)  # Output: 1960

def usage_of_dict1():
    key_val: dict[str,str] = {"key1": "value1", "key2": "value2", "key3": "value3"}
    print(key_val)

    # Accessing dictionary elements by key
    for key in key_val:
        print(f"Key: {key}, Value: {key_val[key]}")

    # Nested dictionary
    config = {
        "db": {"host": "localhost", "port": 5432},
        "cache": {"ttl": 3600}
    }
    for key, value in config.items():
        print(f"Key: {key}, Value: {value}")

    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    d = dict(zip(keys, values))

    for key,val in d.items():
        print(f"Key: {key}, Value: {val}")

    some_val = d["a"]
    print(f"Value of a: {some_val}" )

    # The following line will raise a KeyError
    # some_val = d["d"]
    # print(f"Value of a: {some_val}" )
    # To solve the above problem
    some_val = d.get("d") # Correct
    some_val = d.get("d", "some default value")
    print(f"Value of a: {some_val}" )

    # Merge two dictionaries
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    merged = dict1 | dict2  # {'a': 1, 'b': 3, 'c': 4}

    # Dynamically create dictionary
    data: dict[str,int] = {}
    for i in range(5):
        data[f"key_{i}"] = i * 10
    # {'key_0': 0, 'key_1': 10, 'key_2': 20, 'key_3': 30, 'key_4': 40}
    print(f"Data------>{data}")


if __name__ == '__main__':
    # tuple_ops1()
    # usage_of_named_tuple()
    usage_of_dict1()




