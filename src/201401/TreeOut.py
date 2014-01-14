#coding=utf-8
__author__ = 'jesse'


class Node(object):
    def __init__(self, name):
        self.name = name
        super(Node, self).__init__()

    def visit(self):
        return self.name


class Node1(Node):
    def __init__(self, name, node1):
        self.n1 = node1
        super(Node1, self).__init__(name)

    def visit(self):
        return self.name+'[' + self.n1.visit() + ']'


class Node2(Node):
    def __init__(self, name, node1, node2):
        self.n1, self.n2 = node1, node2
        super(Node2, self).__init__(name)

    def visit(self):
        return self.name+'[' + self.n1.visit() + ', ' + self.n2.visit() + ']'


class Node3(Node):
    def __init__(self, name, node1, node2, node3):
        self.n1, self.n2, self.n3 = node1, node2, node3
        super(Node3, self).__init__(name)


class TreeOut(object):
    def __init__(self, root):
        self.root = root#Node2('Hello', Node2('world1', Node('1'), Node('2')), Node2('world2', Node('1'), Node('2')))

    def visit(self):
        return self.root.visit()


if __name__ == '__main__':
    t = TreeOut()

