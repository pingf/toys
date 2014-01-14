from unittest import main, TestCase

__author__ = 'jesse'

from TreeOut import *


class TestTreeOut(TestCase):
    def setUp(self):
        pass#self.tree = TreeDataOut()

    def tearDown(self):
        pass#self.tree = None

    def test_simple_node_out(self):
        tree = TreeOut(Node('123'))
        self.assertEqual(tree.root.visit(), '123')
    def test_node2_out_should_be_more_complex(self):
        tree = TreeOut(Node2('Hello', Node2('world1', Node('1'), Node('2')), Node2('world2', Node('3'), Node('4'))))
        self.assertEqual(tree.root.visit(), 'Hello[world1[1, 2], world2[3, 4]]')


if __name__ == '__main__':
    main()