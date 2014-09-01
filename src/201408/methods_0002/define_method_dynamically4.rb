class A
  def self.def_comp(m)
    #self.send(:define_method,m) do |*x|
    define_method(m) do |*x|
      puts 'hello world'
      x.each{|x|puts x}
    end
  end
  def_comp :test 
  
end

a=A.new
a.test 1
A.def_comp(:test2)
a.test2 2,3,4

puts [1,2,3]
p [1,2,3]

