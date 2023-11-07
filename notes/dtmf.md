# OOP-Quiz

After defining a class with an `__init__` method, every object
declared as a class type is initialized with attributes as defined
by the `__init__` method.

Class literals are accessible by the class itself or any instances (objects)
of that particular class.

---
What is OOP?

A programming paradigm that focuses on organizing code around objects and their interactions

* Classes and Objects: A class is a template that defines the structure and
behaviour of objects. Objects are individual entities, that are instances of the
class

* Data encapsulation: Instances of a class encapsulate data and behavior. The attributes
store data specific to an instance, and the methods define the behaviour or
actions that the instance can perform.

* Inheritance: Inheritance allows you to create a new class that is a
specialized version of an existing parent class. The new class inherits
attributes and methods of the parent class, and can even override them.
In python you do it as `class SubClass(ParentClass)`

```python
class Vehicle():
    def start_engine(self):
        print("The engine of the vehicle is starting")

class Car(Vehicle):
    # Now there is already the start_engine method for the Car class
    # However, you can override it as:
    def start_engine(self):
        print("Starting car engine")
        super().start_engine() # Call the parent class's implementation of 
                               # start_engine() here
```

* Polymorphism: When a subclass overrides a parent classes method or attribute
with it's own, it behaves in a way unique to itself when a method common to it
and the parent class is called

* Abstraction: The complexity of a system is reduced via modularization

* Composition: The principle of building complex objects by combining simpler
objects or components. This can be done by using other objects as attributes

---
Some dictionary specific methods:

```python
for key, value in my_dict.items():
    print(f'Key: {key}, Value: {value}')
```

```python
dict.get(key, default)
```

```python
del dictionary[key]
```
