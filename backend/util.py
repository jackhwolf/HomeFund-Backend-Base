from types import FunctionType
from functools import wraps, update_wrapper


class BotoException(Exception):
    ''' custom exception '''
    pass


def BotoErrorWrapper(func):
    ''' try to execute function. otherwise throw custom exception
    with function name and error message '''
    @wraps(func)
    def inner_wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            raise BotoException(f"{func.__name__} failed because: " + str(e))
    return update_wrapper(inner_wrapper, func)


class BotoMetaClass(type):
    ''' wrap all methods of a class with the BotoErrorWrapper
    https://stackoverflow.com/questions/11349183/how-to-wrap-every-method-of-a-class
    '''
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType):
                # replace it with a wrapped version
                newClassDict[attributeName] = BotoErrorWrapper(attribute)
        return type.__new__(meta, classname, bases, newClassDict)
