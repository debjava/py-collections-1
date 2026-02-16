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



if __name__ == '__main__':
    # tuple_ops1()
    usage_of_named_tuple()




