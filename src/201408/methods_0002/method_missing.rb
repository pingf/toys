class A
  def method_missing(method,*args)
    puts "first time, define #{method}"
    self.class.send(:define_method,method) do |*args|
      args.each {|x| puts x}
    end
    self.send(method,*args)
  end
end

a=A.new
a.test 1,2,3,4
puts '---'*20
a.test 1,2,3,4

 
