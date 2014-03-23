#coding=utf-8
__author__ = 'jesse'

def before():
    print 'before'
def after():
    print 'after'

def dec_func(method):
    def true_method(method):
        return real_method
    def real_method(self,param):
        before()
        ret = getattr(self,method)(param)
        after()
        return ret
    return true_method

def dec_func2(method):
    def real_dec_func2(self,name):

        print 'before'
        method(self,name)
        print 'after'

    return real_dec_func2



class Demo():
    def __init__(self):
        pass

    def real_test(self,name):
        print '****',name
    @dec_func('real_test')
    def test(self,name):pass

    @dec_func2
    def test2(self,name):
        print name
if __name__ == "__main__":
    t=Demo()
    t.test('123')#test方法是我眩晕状态下写出来的，不用看了
    t.test('456')
    t.test2('789')
