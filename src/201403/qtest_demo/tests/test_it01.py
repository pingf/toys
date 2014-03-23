__author__ = 'jesse'

import sys
import unittest

from PySide.QtGui import *
from PySide.QtTest import *


class Test(unittest.TestCase):
    """Base class for tests
    """
    app = QApplication(sys.argv)

    def setUp(self):
        self.editor = QTextEdit()

    def tearDown(self):
        del self.editor

    def test_overwrite_edit(self):
        self.editor.show()
        self.editor.setPlainText("abcd")
        QTest.keyClicks(self.editor, "1234")
        self.assertEqual(self.editor.toPlainText(), '1234abcd')


if __name__ == '__main__':
    unittest.main()
