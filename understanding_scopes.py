'''
Learnings = 

1. Empty user defined class has 3 more methods than default object class.
These methods are: __dict__, __weakref__, __module__
__dict__ =  A dictionary or other mapping object used to store an object’s (writable) attributes.
__weakref__ = List of weak references for garbage collection.

2. `class A: pass` and `class A(object): pass` are both same.
i.e. Inherting from base object adds no extra functionality.

3. __dict__ assigns attributes to objects with update.

4. Use type(self) in regular methods to access class methods.

'''

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
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        

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
