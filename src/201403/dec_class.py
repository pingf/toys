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
            def true_method(self):
                return real_method
            def real_method(self,name):
                cls.before()
                ret=getattr(self,words)(name)
                cls.after()
                return ret
            return true_method

    def __init__(self):
        pass

    def real_test(self,name):
        print name

    @DecClass.dec_method('real_test')
    def test(self,name): pass

if __name__ == "__main__":
    t=Demo()
    t.test('123')
    t.test('456')
