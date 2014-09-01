class A
  def initialize(singleton_methods) 
    singleton_methods.grep(/^test*/){|m| self.class.def_comp(m)}
  end
  def self.def_comp(m)
    #self.send(:define_method,m) do 
    define_method(m) do |*x|
      puts 'hello world'
      puts m
    end
  end   
end

d=['test1','test2']
 
a=A.new(d) 
a.test1
a.test2
