'''
Learnings - 

__slots__ - Allocate fixed space in RAM to set of attributes.
Raw Strings do not replace backslashes and execute the string as such.
re.match tells if regular expression is matched at beginning of the string.
re.match doesnot return an iterable and just returns the first match. None if no match

(?: does not capture group in match.groups
+ .*
'''
import re

sentence = "hello world, hello all"
sentence2 = "my name is sayam"

pattern = re.compile(r'hello')

match = pattern.match(sentence)
print(match.group(0))

match = pattern.match(sentence2)
print(match)

pattern = re.compile(r"Sa(?:ya)?(m)")
s1 = "Sayam"
match = pattern.match(s1)
print(match)
print("Groups:", match.groups())

class NameParts:
    '''
    in all 4 groups, 0 is the full match
    1. __transform is not captured due to (?:
    2. transform - match starting from __ upto first _
    3. name - should not start with _ after that can have any characters
    '''
    NAME_RE = re.compile(r"^(?:__(?P<transform>[^_]+)_)?(?P<name>[^_].*)$")
    NAME_ERROR_MESSAGE = (
        "Invalid name: `{}`, the correct one should look like: `__transform_name` or `name`, "
        "note only one underscore between the transform and actual name"
    )
    UNTRANSFORMED_NAME_ERROR_MESSAGE = (
        "Invalid name: `{}`, the correct one should look like: " "`name` without leading underscore"
    )
    __slots__ = ("path", "transform_name", "untransformed_name")

    @classmethod
    def is_valid_untransformed_name(cls, name):
        match = cls.NAME_RE.match(name)
        return match is not None and match["transform"] is None

    @classmethod
    def is_valid_name(cls, name):
        match = cls.NAME_RE.match(name)
        return match is not None

    def __init__(self, path, transform_name, untransformed_name):
        self.path = tuple(path)
        self.untransformed_name = untransformed_name
        self.transform_name = transform_name

    @classmethod
    def from_name(cls, name):
        split = name.split("/")
        path, original_name = split[:-1], split[-1]
        match = cls.NAME_RE.match(original_name)
        if not cls.is_valid_name(name):
            raise ValueError(cls.NAME_ERROR_MESSAGE)
        return cls(path, match["transform"], match["name"])

    @property
    def original_name(self):
        if self.is_transformed:
            return "__{}_{}".format(self.transform_name, self.untransformed_name)
        else:
            return self.untransformed_name

    @property
    def full_original_name(self):
        return "/".join(self.path + (self.original_name,))

    @property
    def full_untransformed_name(self):
        return "/".join(self.path + (self.untransformed_name,))

    @property
    def is_transformed(self):
        return self.transform_name is not None

    def __repr__(self):
        return "<NameParts of {}>".format(self.full_original_name)

    def replace_transform(self, transform_name):
        return self.__class__(self.path, transform_name, self.untransformed_name)



def check(name):
    if NameParts.is_valid_name(name):
        match = NameParts.NAME_RE.match(name)
        print(match["transform"], match["name"])
    else:
        print(name, "has no match")

check("sayam")
check("_tiger")
check("__tiger_inzoo")
check("__tiger_in_zoo")
check("__going_to_the_market")
check("__going__to_the_market")