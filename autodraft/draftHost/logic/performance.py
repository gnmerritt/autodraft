
class ReadOnlyCachedAttribute(object):
    '''Computes attribute value and caches it in the instance.
    Source: Python Cookbook
    Author: Denis Otkidach http://stackoverflow.com/users/168352/denis-otkidach
    This decorator allows you to create a property which can be computed once and
    accessed many times. Sort of like memoization
    '''
    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__
    def __get__(self, inst, cls):
        if inst is None:
            return self
        elif self.name in inst.__dict__:
            return inst.__dict__[self.name]
        else:
            result = self.method(inst)
            inst.__dict__[self.name]=result
            return result
    def __set__(self, inst, value):
        raise AttributeError("This property is read-only")
    def __delete__(self,inst):
        del inst.__dict__[self.name]
