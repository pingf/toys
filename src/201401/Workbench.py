#coding=utf-8
__author__ = 'jesse'
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *


class CodeEditor(QsciScintilla):
    def __init__(self, path=None):
        super(CodeEditor, self).__init__()
        self.setUtf8(True) # use utf8
        self.current_file = None
        # self.open()

    def keyPressEvent(self, event):
        key = event.key()
        modifier = event.modifiers()
        if key == Qt.Key_S and modifier & Qt.ControlModifier:
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
        print 'save'
        out_file = QFile(self.current_file)
        if out_file.open(QFile.WriteOnly | QFile.Text):
            out_file.writeData(self.text())
            out_file.close()
            return True
        return False

    def save_as(self, filename):
        pass

    def current_file_path(self):
        return self.current_file


class ProjectModel(QFileSystemModel):
    def columnCount(self, parent=QModelIndex()):
        return super(ProjectModel, self).columnCount() + 1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.DisplayRole:
                return QString("")
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft

        return super(ProjectModel, self).data(index, role)


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
        fileMenu.addAction("&Save", self.test_pass, QKeySequence.Save)
        fileMenu.addAction("Save &As...", self.test_pass, QKeySequence.SaveAs)
        fileMenu.addSeparator()
        fileMenu.addAction("&Close", self.test_pass, "Ctrl+W")
        fileMenu.addSeparator()
        fileMenu.addAction("E&xit", qApp.quit, "Ctrl+Q")
        self.menuBar().addMenu(fileMenu)

    def setup_docks(self):
        dock = QDockWidget("File", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        file_model = ProjectModel()
        file_model.setRootPath("./")
        tree = QTreeView()
        tree.setModel(file_model)
        tree.setRootIndex(file_model.index("./"))
        tree.setCurrentIndex(file_model.index(0, 0))
        tree.hideColumn(1) # for removing Size Column
        tree.hideColumn(2) # for removing Type Column
        tree.hideColumn(3) # for removing Date Modified Column
        tree.setColumnWidth(0, 200)
        tree.setColumnWidth(1, 20)
        tree.doubleClicked.connect(self.test_pass)
        tree.pressed.connect(self.test_pass)

        dock.setWidget(tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        #self.viewMenu.addAction(dock.toggleViewAction())
        self.file_monitor = dock

        dock = QDockWidget("test", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        button1 = QPushButton("click me1")
        button2 = QPushButton("click me2")
        button3 = QPushButton("click me3")
        button1.clicked.connect(self.open)
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
        self.editors = QMdiArea(self)
        self.editors.setViewMode(QMdiArea.TabbedView)
        self.editors.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.editors.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.editors)

    def setup_ui(self):
        self.setup_menus()
        self.setup_docks()
        self.setup_central()
        self.statusBar().show()
        #self.setCentralWidget(self.file_monitor)

    def createMdiChild(self):
        child = CodeEditor()
        self.editors.addSubWindow(child)

        # child.copyAvailable.connect(self.cutAct.setEnabled)
        # child.copyAvailable.connect(self.copyAct.setEnabled)

        return child

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.editors.subWindowList():
            if window.widget().current_file_path() == canonicalFilePath:
                return window
        return None

    def open(self):
        fileName = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.editors.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.open(fileName):
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