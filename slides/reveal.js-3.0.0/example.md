##demo
Slide 1.1

--

## Demo 2
Slide 1.2

--

## Demo 2
Slide 2

--

# **Ruby** and its fellows

--

# Ruby at a Glance

- a Programming Language
- Open Source
- Designed by Yukihiro Matsumoto
- Appeared in 1995
- Stable release 2.1.2 / May 9, 2014
- Cross-platform

```python
def main():
		print('hello')
```

```ruby
require 'webrick'

class Simple < WEBrick::HTTPServlet::AbstractServlet
  def initialize server, color, size
    super server
    @color = color
    @size = size
  end

  def service request, response
    status, content_type, body = 200, 'text/plain', "color is #{@color} and size is #{@size}"

    response.status = status
    response['Content-Type'] = content_type
    response.body = body
  end
```

--

## Ruby Features

- Dynamic typing and duck typing
- Object-oriented
- Functional
- Imperative
- Automatic memory management
- Modules
- Mixins
- Default arguments
- Metaprogramming