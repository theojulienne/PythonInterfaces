__all__ = [ 'interface', 'implements' ]

import inspect

class interface(object):
	@classmethod
	def isImplementedBy( cls, obj ):
		return cls in getattr(obj, '__interfaces__', [])

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

def implements( *interfaceClasses ):
	def implementsDecorator( newClass ):
		for interfaceClass in interfaceClasses:
			assert issubclass( interfaceClass, interface )

			interfaceFunctions = [name for name in dir(interfaceClass) if not name.startswith( '_' )]
			
			# save this interface in the class's interface list
			if not hasattr( newClass, '__interfaces__' ):
				newClass.__interfaces__ = []
			newClass.__interfaces__.append( interfaceClass )
		
			classMethods = dir(newClass)
			for functionName in interfaceFunctions:
				interfaceFunc = getattr( interfaceClass, functionName )
				if interfaceFunc.__module__ != interface.__module__:
					if not functionName in classMethods:
						raise MissingInterfaceMethodException( newClass, functionName, interfaceClass )
					else:
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

