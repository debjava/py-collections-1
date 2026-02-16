from dataclasses import dataclass, field


@dataclass
class Person:
    name: str
    age: int
    city: str


@dataclass(init=True, repr=True, eq=True, order=True)
class Student:
    name: str
    age: int = field(default=0)
    city: str = field(default="")


def usage_1():
    person1 = Person("John", 30, "New York")
    print(f"person object: {person1}")
    print(f"Person Name: {person1.name}")

    s = Student("John")
    s.age = 20
    s.city = "Bangaloe"
    print(f"Student object: {s}")




if __name__ == '__main__':
    usage_1()