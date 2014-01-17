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
        self.assertEqual(tree.root.visit(), 'Hello[world1[1,2],world2[3,4]]')

    def test_split_into_edges(self):
        self.assertEqual(TreeOut.edges('Hello[world1[1,2],world2[3,4]]', []),
                         [('Hello', 'world1'),
                          ('world1', '1'), ('world1', '2'),
                          ('Hello', 'world2'),
                          ('world2', '3'), ('world2', '4')])

    def test_out_for_graphviz(self):
        from mock import MagicMock

        tree = TreeOut(Node2('Hello', Node2('world1', Node('1'), Node('2')), Node2('world2', Node('3'), Node('4'))))
        tree.root.visit = MagicMock(return_value='Hello[world1[1,2],world2[3,4]]')

        ret = tree.graph()
        tree.root.visit.assert_called_once_with()
        self.assertEqual(ret, 'digraph test{\n'
                              'Hello->world1;\n'
                              'world1->1;\n'
                              'world1->2;\n'
                              'Hello->world2;\n'
                              'world2->3;\n'
                              'world2->4;\n'
                              '}')


if __name__ == '__main__':
    main()