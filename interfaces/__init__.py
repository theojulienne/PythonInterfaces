__all__ = [ 'interface', 'implements' ]

import inspect

class interface(object):
	pass

class MissingInterfaceMethodException(Exception):
	def __init__( self, newClass, functionName, interfaceClass ):
		msg = "%s does not implement '%s' from %s" % \
			( newClass.__name__, functionName, interfaceClass.__name__ )
		super(MissingInterfaceMethodException, self).__init__( msg )

class IncompatibleMethodException(Exception):
	def __init__( self, interfaceClass, interfaceSig, newClass, implementationSig ):
		msg = "%s implements %s but %s expects %s" % \
			( newClass.__name__, implementationSig, \
			  interfaceClass.__name__, interfaceSig )
		super(IncompatibleMethodException, self).__init__( msg )

def getMethodSignature( method ):
	argList = ''
	
	args, varargs, keywords, defaults = inspect.getargspec( method )
	
	argList = ', '.join( args )
	
	callSpec = "%s( %s )" % (method.__name__, argList)
	
	return callSpec

def implements( interfaceClass ):
	assert issubclass( interfaceClass, interface )
	
	interfaceFunctions = [name for name in dir(interfaceClass) if not name.startswith( '_' )]
	
	def implementsDecorator( newClass ):
		# save this interface in the class's interface list
		if not hasattr( newClass, '__interfaces__' ):
			newClass.__interfaces__ = []
		newClass.__interfaces__.append( interfaceClass )
		
		classMethods = dir(newClass)
		for functionName in interfaceFunctions:
			if not functionName in classMethods:
				raise MissingInterfaceMethodException( newClass, functionName, interfaceClass )
			else:
				interfaceFunc = getattr( interfaceClass, functionName )
				implementFunc = getattr( newClass, functionName )
				
				interfaceSig = getMethodSignature( interfaceFunc )
				implementSig = getMethodSignature( implementFunc )
				
				# make sure the signatures match (including names)
				if interfaceSig != implementSig:
					raise IncompatibleMethodException( \
						interfaceClass, interfaceSig, \
						newClass, implementSig )
				
				# copy over the docstring unless it already has one
				if implementFunc.__func__.__doc__ is None:
					implementFunc.__func__.__doc__ = interfaceFunc.__func__.__doc__
			
					
		return newClass
	return implementsDecorator


if __name__ == '__main__':
	class IBar(interface):
		def bar( self, a, b, c ):
			"""blah blah blah"""

	class IBaz(interface):
		def baz( self, b, z ):
			"""Baz from IBaz"""

	@implements(IBar)
	@implements(IBaz)
	class Foo(object):
		def bar( self, a, b, c ):
			pass
			
		def baz( self, b, z ):
			pass
	
	print Foo.__interfaces__
	print Foo.bar.__doc__
	print Foo.baz.__doc__

	#f = Foo( )