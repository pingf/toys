# Inappropriate Intimacy 

two classes have duplicated parts

---
```ruby
class T1
	def test1
	end
	def test2
	end
	def test3
	end
end
class T2
	def test1
	end
	def test4
	end
end
	
```
---
```ruby
class T0
	def test1
	end
end
class T1 < T0
	def test2
	end
	def test3
	end
end
class T2 < T0
	def test4
	end
end
	
```
---

Bidirectional Association

---
```ruby
class Client
	def initialize department, manager 
		@department = department
		@manager = manager
	end
end

class person
	def initialize(department)
		@department = department
	end
end

class Department
	def employ person
		@manager ||= person
	end
end
```

---

Hide Delegate => Unidirectional Association

---
```ruby
class Client
	def initialize manager
		@manager = manager
	end
end

class person
	attr_reader :department
	def initialize(department)
		@department = department
	end
end

class Department
end
```
---

Sometimes classes become far too intimate & spend too much time delving into each other's private parts.

---

```ruby
class Parent
	def pub_method
		...
	end
	private
	def pri_method
		...
	end
end

class Child < Parent
	def test
		a = pub_method
		 
		b = pri_method
	end
end
```

---

```ruby

class A
	def pub_method
		...
	end
	private
	def pri_method
		...
	end
end

class B
	def initialize
		@a = A.new
	end
	def test
		a = @a.pub_method
	end
end

```


