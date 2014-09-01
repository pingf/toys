class A
  define_method("test") do |x|
    puts x
  end
  
  define_method "test2" do |x|
    puts x
  end
  
  define_method :test3 do |x|
    puts x
  end
end

a=A.new
a.test 5
a.test2 6
a.test3 7

def a.test4(x)
  puts x
end 
a.test4 8
