'''
Learnings = 

1. Empty user defined class has 3 more methods than default object class.
These methods are: __dict__, __weakref__, __module__
__dict__ =  A dictionary or other mapping object used to store an object’s (writable) attributes.
__weakref__ = List of weak references for garbage collection.

2. `class A: pass` and `class A(object): pass` are both same.
i.e. Inherting from base object adds no extra functionality.

3. __dict__ assigns attributes to objects with update.

4. Use type(self) or self.__class__ in regular methods to access class methods.

5. The threading.local() function creates an object capable of hiding values from view in separate threads.

6. Use __enter__ and __exit__ to make something as decorator
'''

import random, threading

class A:
    pass

class B:
    pass

class Inherited_A(object):
    pass

def find_intersection(X, Y):
    set1 = set(dir(X))
    set2 = set(dir(Y))
    intersection = set1 & set2
    print(f"\nLen of all attributes of {X.__name__}:", len(set1))
    print(f"Len of all attributes of {Y.__name__}:", len(set2))
    print("Len of intersected portion:", len(intersection))

    if len(intersection) < len(set1):
        print("Extra attributes in class are:", set1-set2)


class Scope:

    _leaf = object()
    context = threading.local()

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __enter__(self):
        type(self).get_contexts().append(self)
        print("Self.name right now is:", self.name)
        for element in type(self).context.stack:
            print(element.name)
        # print("Stack so far is:", type(self).context.stack)
        return self

    def __exit__(self, typ, value, traceback):
        type(self).get_contexts().pop()

    def __getattr__(self, item):
        return self.__dict__.get(item)

    @classmethod
    def get_contexts(cls):
        if not hasattr(cls.context, "stack"):
            cls.context.stack = []
        return cls.context.stack

    @classmethod
    def variable_name(cls, name: str):
        """
        Generate PyMC4 variable name based on name scope we are currently in.

        Parameters
        ----------
        name : str|None
            The desired target name for a variable, can be any, including None

        Returns
        -------
        str : scoped name

        Examples
        --------
        >>> with Scope(name="inner"):
        ...     print(Scope.variable_name("leaf"))
        inner/leaf
        >>> with Scope(name="inner"):
        ...     with Scope():
        ...         print(Scope.variable_name("leaf1"))
        inner/leaf1

        empty name results in None name
        >>> assert Scope.variable_name(None) is None
        >>> assert Scope.variable_name("") is None
        """
        value = "/".join(map(str, cls.chain("name", leaf=name, drop_none=True)))
        if not value:  # For None and empty strings
            return None
        else:
            return value
        
    @classmethod
    def chain(cls, attr, *, leaf=_leaf, predicate=lambda _: True, drop_none=False):
        for c in cls.get_contexts():
            if predicate(c):
                val = getattr(c, attr)
                if drop_none and val is None:
                    continue
                else:
                    yield val
        if leaf is not cls._leaf:
            if not (drop_none and leaf is None):
                yield leaf
        

if __name__ == "__main__":
    # With another default class
    find_intersection(A, B)

    # With default object()
    find_intersection(A, object)

    # Inheriting object class
    find_intersection(A, Inherited_A)

    # Playing with Scopes
    s = Scope(name="Sayam")
    if hasattr(s, 'name'):
        print("My name is:", s.name)

    with Scope(name="Sayam"):
        with Scope(name="kumar"):
            pass
