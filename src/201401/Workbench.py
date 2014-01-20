#coding=utf-8
__author__ = 'jesse'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import os


class CodeEditor(QsciScintilla):
    def __init__(self, path=None):
        super(CodeEditor, self).__init__()
        self.setUtf8(True) # use utf8
        self.current_file = None
        # self.open()
    def set_current_file(self,filename):
        self.current_file = filename
    def keyPressEvent(self, event):
        key = event.key()
        modifier = event.modifiers()
        if (key == Qt.Key_S) and (modifier & Qt.ControlModifier):
            self.save()
        return super(CodeEditor, self).keyPressEvent(event)

    def open(self, filepath):
        if not filepath:
            self.setText("")
            return 0
        in_file = QFile(filepath)
        if in_file.open(QFile.ReadOnly | QFile.Text):
            text = in_file.readAll()
            try:
                text = str(text, encoding='utf-8')
            except TypeError:
                text = str(text)
            self.setText(text)
            in_file.close()
            self.current_file = filepath
            return True
        return False

    def save(self):
        self.save_as(self.current_file)


    def save_as(self, filename):
        assert filename != None
        out_file = QFile(filename)
        if out_file.open(QFile.WriteOnly | QFile.Text):
            out_file.writeData(self.text())
            out_file.close()
            self.current_file = filename
            return True
        return False

    def current_filepath(self):
        return self.current_file


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

        self.buddy = None
        self.doubleClicked.connect(self.open_file)

    def set_buddy(self, buddy):
        self.buddy = buddy

    def open_file(self, index):
        path = self.model().filePath(index)
        print path
        return self.buddy.open_file(path)


class MDIEditor(QMdiArea):
    def __init__(self, parent=None):
        super(MDIEditor, self).__init__(parent)
        self.setViewMode(QMdiArea.TabbedView)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def create_code_child(self):
        child = CodeEditor()
        self.addSubWindow(child)
        return child


    def find_child(self, name):
        canonical_filepath = QFileInfo(name).canonicalFilePath()
        for window in self.subWindowList():
            if window.widget().current_filepath() == canonical_filepath:
                return window
        return None

    def open_file(self, filename):
        if filename:
            existing = self.find_child(filename)
            if existing:
                self.setActiveSubWindow(existing)
                return
            child_create_map = {"code": self.create_code_child}
            child_type = "code"
            child = child_create_map[child_type]()
            if child.open(filename):
                child.set_current_file(filename)
                self.subWindowList()[-1].setWindowTitle(os.path.basename(str(filename)))
                child.show()
                return True
            else:
                child.close()
        return False

    def open(self):
        filename = QFileDialog.getOpenFileName(self)
        return self.open_file(filename)

class Workbench(QMainWindow):
    def __init__(self):
        super(Workbench, self).__init__()
        self.navigators = None
        self.editors = None
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
        dock = QDockWidget("File", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        file_model = FileModel()
        tree = FileTreeView(file_model,'./',self)
        tree.setModel(file_model)

        dock.setWidget(tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.file_monitor = dock

        dock = QDockWidget("test", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        button1 = QPushButton("click me1")
        button2 = QPushButton("click me2")
        button3 = QPushButton("click me3")
        self.button1,self.button2,self.button3=button1,button2,button3
        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        widget = QWidget()
        widget.setMaximumWidth(200)
        widget.setLayout(vbox)
        dock.setWidget(widget)
        self.buttons = dock

        dock = QDockWidget("test", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        dock.setWidget(QTextEdit())

        self.addDockWidget(Qt.DockWidgetArea(2), dock)
        self.tabifyDockWidget(self.file_monitor, self.buttons)

    def setup_central(self):
        self.editors = MDIEditor(self)

        self.setCentralWidget(self.editors)

    def setup_ui(self):
        self.setup_menus()
        self.setup_docks()
        self.setup_central()

        self.file_monitor.widget().set_buddy(self.editors)
        self.button1.clicked.connect(self.editors.open)
        self.statusBar().show()

    def open(self):
        filename = QFileDialog.getOpenFileName(self)
        return self.open_file(filename)

    def open_file(self, filename):
        if filename:
            existing = self.editors.find_child(filename)
            if existing:
                self.editors.setActiveSubWindow(existing)
                return

            child = self.editors.create_child("code")
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