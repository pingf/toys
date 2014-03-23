#coding=utf-8
__author__ = 'jesse'


class Demo():
    class DecClass():
        @staticmethod
        def before():
            print 'before'
        @staticmethod
        def after():
            print 'after'
        @classmethod
        def dec_method(cls,words):
            def true_method(method):
                return real_method
            def real_method(self,name):
                cls.before()
                ret=getattr(self,words)(name)
                cls.after()
                return ret
            return true_method

        @classmethod
        def dec_func2(cls,method):
            def real_dec_func2(self,name):


                cls.before()
                method(self,name)

                cls.after()

            return real_dec_func2


    def __init__(self):
        pass

    def real_test(self,name):
        print name

    @DecClass.dec_method('real_test')
    def test(self,name): pass


    @DecClass.dec_func2
    def test2(self,name):
        print name

if __name__ == "__main__":
    t=Demo()
    t.test('123')#test方法是我眩晕状态下写出来的，不用看了
    t.test('456')
    t.test2('789')
