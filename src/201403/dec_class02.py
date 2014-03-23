__author__ = 'jesse'

def before():
    print 'before'
def after():
    print 'after'

def dec_func(method):
    def true_method(self):
        return real_method
    def real_method(self,param):
        before()
        ret = getattr(self,method)(param)
        after()
        return ret

    return true_method
class Demo():
    def __init__(self):
        pass

    def real_test(self,name):
        print '****',name
    @dec_func('real_test')
    def test(self,name):pass

if __name__ == "__main__":
    t=Demo()
    t.test('123')
    t.test('456')
