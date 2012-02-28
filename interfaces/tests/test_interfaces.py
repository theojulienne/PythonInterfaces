import pytest

from interfaces import *
import interfaces

def test_basic_interfaces():
	class IBar(interface):
		def bar( self, a, b, c ):
			"""blah blah blah"""

	class IBaz(interface):
		def baz( self, b, z ):
			"""Baz from IBaz"""

	@implements(IBar)
	@implements(IBaz)
	class Foo(object):
		def bar( self, a, b, c ): pass
		def baz( self, b, z ): pass
		
	
	@implements(IBar)
	class Qux(object):
		def bar( self, a, b, c ): pass
		def baz( self, b, z ): pass

	assert IBar.isImplementedBy( Foo )
	assert IBaz.isImplementedBy( Foo )
	assert not IBaz.isImplementedBy( Qux )
	assert not IBaz.isImplementedBy( int )
	assert IBar.isImplementedBy( Foo() )
	assert IBaz.isImplementedBy( Foo() )
	assert not IBaz.isImplementedBy( Qux() )
	assert not IBaz.isImplementedBy( 1 )
	assert Foo.bar.__doc__ == "blah blah blah"
	assert Foo.baz.__doc__ == "Baz from IBaz"

def test_chained_interfaces():
	class IBar(interface):
		def bar( self, a, b, c ):
			"""blah blah blah"""

	class IBaz(interface):
		def baz( self, b, z ):
			"""Baz from IBaz"""

	@implements(IBaz, IBar)
	class Foo(object):
		def bar( self, a, b, c ): pass
		def baz( self, b, z ): pass

	assert IBar.isImplementedBy( Foo )
	assert IBaz.isImplementedBy( Foo )
	assert Foo.bar.__doc__ == "blah blah blah"
	assert Foo.baz.__doc__ == "Baz from IBaz"

def test_bad_interfaces():
	class IBar(interface):
		def qux( self, n ):
			"""blah blah"""
		
		def bar( self, a, b, c ):
			"""blah blah blah"""

	class IBaz(interface):
		def baz( self, b, z ):
			"""Baz from IBaz"""
	
	with pytest.raises(interfaces.MissingInterfaceMethodException):
		@implements(IBar)
		@implements(IBaz)
		class Foo(object):
			def bar( self, a, b, c ): pass
			def baz( self, b, z ): pass
	
	with pytest.raises(interfaces.IncompatibleMethodException):
		@implements(IBar)
		@implements(IBaz)
		class Foo(object):
			def qux( self ): pass
			def bar( self, a, b, c ): pass
			def baz( self, b, z ): pass
