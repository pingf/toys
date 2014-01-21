#coding=utf-8
__author__ = 'jesse'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import os


class CodeEditor(QsciScintilla):
    def __init__(self, name='untitled'):
        super(CodeEditor, self).__init__()
        self.setUtf8(True) # use utf8
        self.filename = name

    def set_current_file(self, filename):
        self.filename = filename

    def current_filepath(self):
        return self.filename

    def keyPressEvent(self, event):
        key = event.key()
        modifier = event.modifiers()
        if key == Qt.Key_S and modifier & Qt.ControlModifier:
            self.save()
        return super(CodeEditor, self).keyPressEvent(event)

    def open(self, filename):
        if not filename:
            self.setText("")
            return 0
        in_file = QFile(filename)
        if in_file.open(QFile.ReadOnly | QFile.Text):
            text = in_file.readAll()
            try:
                text = str(text, encoding='utf-8')
            except TypeError:
                text = str(text)
            self.setText(text)
            in_file.close()
            self.filename = filename
            return True
        return False

    def save(self):
        self.save_as(self.current_filepath)

    def save_as(self, filename=None):
        if filename is not None:
            out_file = QFile(filename)
            if out_file.open(QFile.WriteOnly | QFile.Text):
                out_file.writeData(self.text())
                out_file.close()
                self.current_filepath = filename
                return True
        return False


class FileModel(QFileSystemModel):
    def columnCount(self, parent=QModelIndex()):
        return super(FileModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.DisplayRole:
                return QString("")
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft
        return super(FileModel, self).data(index, role)


class FileTreeView(QTreeView):
    def __init__(self, model, path, parent=None):
        super(FileTreeView, self).__init__(parent)
        model.setRootPath(path)
        self.setModel(model)
        self.setRootIndex(model.index(path))
        self.setCurrentIndex(model.index(0, 0))
        self.hideColumn(1) # for removing Size Column
        self.hideColumn(2) # for removing Type Column
        self.hideColumn(3) # for removing Date Modified Column
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 20)

    def set_buddy(self, buddy):
        self.buddy = buddy


class MDIEditor(QMdiArea):
    def __init__(self, parent=None):
        super(MDIEditor, self).__init__(parent)
        self.setViewMode(QMdiArea.TabbedView)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def create_code_child(self, filename):
        child = CodeEditor()
        subwin = self.addSubWindow(child)
        print subwin, filename
        subwin.setWindowTitle(os.path.basename(str(filename)))
        return child

    def find_child(self, name):
        canonical_filepath = QFileInfo(name).canonicalFilePath()
        for window in self.subWindowList():
            print window.widget()
            if window.widget().current_filepath() == canonical_filepath:
                return window
        return None


class Dock(QDockWidget):
    def __init__(self, name='dock', parent=None):
        super(QDockWidget, self).__init__(name, parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)


class TestToolBox(QWidget):
    def __init__(self, parent=None):
        super(TestToolBox, self).__init__(parent)
        self.buttons = [QPushButton("button 0"),
                        QPushButton("button 1"),
                        QPushButton("button 2"),
                        QPushButton("button 3"),
                        QPushButton("button 4"),
                        QPushButton("button 5"),
                        QPushButton("button 6"),
                        QPushButton("button 7")]

        vbox = QVBoxLayout()
        for i in range(8):
            vbox.addWidget(self.buttons[i])
        self.setMaximumWidth(200)
        self.setLayout(vbox)

    def button(self, num=0):
        return self.buttons[0]


class Workbench(QMainWindow):
    def __init__(self):
        super(Workbench, self).__init__()
        self.setup_ui()
        # print self.__dict__.keys()
        # print [method for method in dir(self) if callable(getattr(self, method))]

    def test_pass(self):
        pass

    def setup_menus(self):
        fileMenu = QMenu("&File", self)
        fileMenu.addAction("&New file", self.test_pass, "Ctrl+1")
        fileMenu.addAction("&Open directory...", self.test_pass, "Ctrl+O")
        fileMenu.addSeparator()
        #fileMenu.addAction("&Save", self.test_pass, QKeySequence.Save)
        #fileMenu.addAction("Save &As...", self.test_pass, QKeySequence.SaveAs)
        fileMenu.addSeparator()
        fileMenu.addAction("&Close", self.test_pass, "Ctrl+W")
        fileMenu.addSeparator()
        fileMenu.addAction("E&xit", qApp.quit, "Ctrl+Q")
        self.menuBar().addMenu(fileMenu)

    def setup_docks(self):
        file_monitor_dock = Dock("File", self)
        file_model = FileModel()
        tree = FileTreeView(file_model, './', file_monitor_dock)
        file_monitor_dock.setWidget(tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, file_monitor_dock)
        self.file_monitor = tree

        tool_box_dock = Dock("test", self)
        widget = TestToolBox()
        tool_box_dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, tool_box_dock)
        self.tool_box = widget

        #self.addDockWidget(Qt.DockWidgetArea(2), dock)
        #self.tabifyDockWidget(file_monitor_dock, tool_box_dock)

    def setup_central(self):
        self.editors = MDIEditor(self)

        self.setCentralWidget(self.editors)

    def setup_signals(self):
        self.tool_box.button(0).clicked.connect(self.open)
        self.file_monitor.doubleClicked.connect(self.open_file_from_file_monitor)


    def setup_ui(self):
        self.setup_menus()
        self.setup_docks()
        self.setup_central()

        self.statusBar().show()

        self.setup_signals()


    def open(self):
        filename = QFileDialog.getOpenFileName(self)
        return self.open_file(filename)


    def open_file_from_file_monitor(self, index):
        path = self.file_monitor.model().filePath(index)
        return self.open_file(path)

    def open_file(self, filename):
        if filename:
            existing = self.editors.find_child(filename)
            if existing:
                self.editors.setActiveSubWindow(existing)
                return

            child = self.editors.create_code_child(filename)
            if child.open(filename):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()


if __name__ == '__main__':
    # bench = Workbench()
    # print hasattr(bench, "editor")

    import sys

    app = QApplication(sys.argv)
    mainWin = Workbench()
    mainWin.show()
    sys.exit(app.exec_())