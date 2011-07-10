Usage Example
-------------

    >>> from interfaces import *
    >>> class IFoo(interface):
    ...    def foo( self, a, b, c ):
    ...       """Does a foo"""
    ... 
    >>> @implements(IFoo)
    ... class Foo(object):
    ...    pass
    ... 
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
      File "interfaces/__init__.py", line 46, in implementsDecorator
        raise MissingInterfaceMethodException( newClass, functionName, interfaceClass )
    interfaces.MissingInterfaceMethodException: Foo does not implement 'foo' from IFoo
    >>> @implements(IFoo)
    ... class Foo(object):
    ...    def foo( self ):
    ...       pass
    ... 
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
      File "interfaces/__init__.py", line 58, in implementsDecorator
        newClass, implementSig )
    interfaces.IncompatibleMethodException: Foo implements foo( self ) but IFoo expects foo( self, a, b, c )
    >>> @implements(IFoo)
    ... class Foo(object):
    ...    def foo( self, a, b, c ):
    ...       pass
    ... 
    >>> f = Foo( )
    >>> help(f.foo)
    Help on method foo in module __main__:
    
    foo(self, a, b, c) method of __main__.Foo instance
        Does a foo
    
