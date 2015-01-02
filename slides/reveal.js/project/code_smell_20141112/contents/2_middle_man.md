# The Middle Man

whether the director use a diary or atoms to keep track of her appointments.

---

# I don't care

---
```ruby
class Appointment
	...
	def track
		...
	end
end

class Diary
	....
	def track
		@appointment.track
	end
end

class Director
	...
	def track
		....
		@diray.track
	end
end
```
---

- remove middle man
- inline methods
- replace delegation with hierarchy
- turn the real object into a module and include it in the middle man

---

```ruby
class Person
	def name
		'Jesse'
	end
end

class Employee 
	def initialize
		@person =  Person.new
	end
	def name
		@person.name
	end
end
```

---

```ruby
class Person
	def name
		'Jesse'
	end
end

class Employee < Person 
end

```


---

You can kill the wombat with a weapon

You can kill the wombat with a knife

You can kill the wombat with a gun 

