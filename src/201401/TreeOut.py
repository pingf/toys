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
        return self.name + '[' + self.n1.visit() + ']'


class Node2(Node):
    def __init__(self, name, node1, node2):
        self.n1, self.n2 = node1, node2
        super(Node2, self).__init__(name)

    def visit(self):
        return self.name + '[' + self.n1.visit() + ',' + self.n2.visit() + ']'


class Node3(Node):
    def __init__(self, name, node1, node2, node3):
        self.n1, self.n2, self.n3 = node1, node2, node3
        super(Node3, self).__init__(name)


class TreeOut(object):
    def __init__(self, root):
        self.root = root#Node2('Hello', Node2('world1', Node('1'), Node('2')), Node2('world2', Node('1'), Node('2')))

    def visit(self):
        return self.root.visit()

    @staticmethod
    def split(input):
        cnt = 0
        sp_list = []
        st = 0
        for i, v in enumerate(input):
            if v == '[':
                cnt += 1
            elif v == ']':
                cnt -= 1
            elif v == ',':
                if cnt == 0:
                    sp_list.append(input[st:i])
                    st = i + 1
        sp_list.append(input[st:])
        return sp_list

    @staticmethod
    def nodename(input):
        id = input.find('[')
        if id < 0:
            return input
        for i, v in enumerate(input):
            if v == '[' or v == ',' or v == ']':
                return input[:i]
        return None

    @staticmethod
    def nodebody(input):
        if id < 0:
            return input
        return input[input.index('[') + 1:-1]

    @staticmethod
    def edges(input, edges):
        #'Hello[world1[1[11,22],2],world2[3,4]]'
        name = TreeOut.nodename(input)
        body = TreeOut.nodebody(input)
        # print name,body
        l = TreeOut.split(body)
        # print l
        for i, v in enumerate(l):
            edges.append((name, TreeOut.nodename(v)))
            #for i,v in enumerate(l):
            id = v.find('[')
            if id < 0:
                continue
            TreeOut.edges(v, edges)
        return edges


if __name__ == '__main__':
    m = []
    t = TreeOut.edges('Hello[world1[1,2],world2[3,4]]', m)
    print m
    print m == t

