module Wrapper
  def before(pattern)       
    self.instance_methods.grep(pattern[:p]) do |m|                            
      alias_method :"__before_#{m[0]}__#{m[-1]}_tmp__", m                      
      self.send(:define_method,m) do |*args|                     
        do_before(*args)                                              
        self.send(:"__before_#{m[0]}__#{m[-1]}_tmp__", *args)         
      end
    end
  end
  def after(pattern)
    self.instance_methods.grep(pattern[:p]) do |m|
      alias_method :"__after_#{m[0]}__#{m[-1]}_tmp__", m
      self.send(:define_method,m) do |*args|
        self.send(:"__after_#{m[0]}__#{m[-1]}_tmp__", *args)
        do_after(*args)
      end
    end
  end
end

class Query
  def query1(x)
    puts "select * from A#{x};"
  end
  def query2(x)
    puts "select * from B#{x};"
  end
end

class Query
  def do_before(*args)
    puts 'connect'
  end

  def do_after(*args)
    puts 'release'
  end
  extend Wrapper
  before :p => /^query*/
  after :p => /^query*/
end

t=Query.new
t.query1(1)
puts "--------------"
t.query2(2)
puts "--------------"
t.query1(3)
puts "--------------"
t.query2(4)