__author__ = 'jesse'
def audit_action(function_to_decorate):
    def wrapper(*args, **kw):
        # Calling your function
        output = function_to_decorate(*args, **kw)
        # Below this line you can do post processing
        print "In Post Processing...."
    return wrapper


@audit_action
def test():
    print 'here'


if __name__=='__main__':
    test()