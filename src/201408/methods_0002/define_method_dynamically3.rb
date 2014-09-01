class A
  def initialize(n)    
    self.class.send(:define_method,n) { puts "some method #{n}" }    
  end
end

a = A.new('a')
a2 = A.new('a2')
a.a
a.a2


puts '---'*20


class B
  def initialize(n)    
    self.define_singleton_method(n) { puts "some method #{n}" }    
  end
end

b = B.new('b')
b2 = B.new('b2')
b.b

begin
b.b2
rescue => e
  puts e
end

b2.b2