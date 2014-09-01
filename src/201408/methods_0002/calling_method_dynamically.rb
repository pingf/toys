class A
  def test(param)
    puts param
  end
end

a = A.new
a.test('test')
puts '---'*20

a.send(:test,'hello')
p :test.class
puts '---'*20

a.send('test','again')
p 'test'.class
puts '---'*20

a.send('test'.to_sym,'123')
p 'test'.to_sym.class
puts '---'*20

a.send(:'test','456')
p :'test'.class
puts '---'*20

p '---'*20



