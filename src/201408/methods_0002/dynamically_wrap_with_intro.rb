class Foo
  def test1
    puts 1
  end
  
  def test2(x)
    puts x  
  end
  
  def test3(x,y,z)
    puts x,y,z
    puts @test
  end
end

module SuperWrapper
  @test=123
  def def_comp(m)
    self.send(:define_method,m) do |*x|
      puts 'connect~~~' 
      @test=123
      self.class.superclass.instance_method(m).bind(self).call *x
      @test=0
      puts 'release~~~'
    end
  end   
  def wrap_pattern(p)
    self.instance_methods.grep(p){|m| self.def_comp(m) }
  end
  
end

class Bar<Foo
  extend SuperWrapper
  def initialize
    self.class.wrap_pattern(/^test*/)
  end
end



f=Foo.new
f.test1 
f.test2 2
f.test3 3,4,5
puts '---'*20
b=Bar.new
b.test1 
b.test2 4
b.test3 5,6,7
 
