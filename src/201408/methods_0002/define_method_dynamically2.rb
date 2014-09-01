
# class A
  # define_method("test") do |x|
    # define_method "test2" do |x|
      # puts x
    # end
  # end
# end

class A
  define_method("test") do |x|
    puts x
    #WRONG WAY: self.class.define_method("test2")
    #WRONG WAY: A.define_method("test2") do |x|
    self.class.send(:define_method,"test2") do |x|
      puts x
    end
  end
end

a=A.new
a.test 4 
a.test2 5 
 
 
