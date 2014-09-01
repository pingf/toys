class A
  def method_missing(method,*args)
    puts 'method :#{method}'
    args.each{|x| puts x}
  end
end

a=A.new
a.test 1,2,3,4

 
