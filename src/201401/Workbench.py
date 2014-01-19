#coding=utf-8
__author__ = 'jesse'
from PyQt4.QtGui import *
from PyQt4.QtCore import *


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
        tree.setColumnWidth(1, 40)
        tree.doubleClicked.connect(self.test_pass)
        tree.pressed.connect(self.test_pass)
        tree.setStyleSheet(
            """
             QHeaderView::section {
     background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #616161, stop: 0.5 #505050,
                                       stop: 0.6 #434343, stop:1 #656565);
     color: white;
     padding-left: 4px;
     border: 1px solid #6c6c6c;
 }

 QHeaderView::section:checked
 {
     background-color: red;
 }

 /* style the sort indicator */
 QHeaderView::down-arrow {
     image: url(down_arrow.png);
 }

 QHeaderView::up-arrow {
     image: url(up_arrow.png);
 }
    QMainWindow::separator  {
        background: yellow;
        width: 10px; /* when vertical */
        height: 0px; /* when horizontal */
    }

    QMainWindow::separator:hover  {
        background: red;
    }
 QFrame, QLabel, QToolTip {
     border: 2px solid green;
     border-radius: 4px;
     padding: 2px;
     background-image: url(images/welcome.png);
 }

  QGroupBox {
     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #E0E0E0, stop: 1 #FFFFFF);
     border: 2px solid gray;
     border-radius: 5px;
     margin-top: 1ex; /* leave space at the top for the title */
 }

 QGroupBox::title {
     subcontrol-origin: margin;
     subcontrol-position: top center; /* position at the top center */
     padding: 0 3px;
     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #FFOECE, stop: 1 #FFFFFF);
 }
            """)

        dock.setWidget(tree)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        #self.viewMenu.addAction(dock.toggleViewAction())
        self.file_monitor = dock

        dock = QDockWidget("Paragraphs", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
            "28 days.",
            "We have dispatched those items that were in stock. The rest of "
            "your order will be dispatched once all the remaining items "
            "have arrived at our warehouse. No additional shipping "
            "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
            "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
            "your order anyway. We'll add this underpayment to your next "
            "bill.",
            "Unfortunately you did not send enough money. Please remit an "
            "additional $. Your order will be dispatched as soon as the "
            "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
            "items, or should we return the excess to you?"))
        dock.setWidget(self.paragraphsList)
        #self.addDockWidget(Qt.RightDockWidgetArea, dock)
        #self.viewMenu.addAction(dock.toggleViewAction())

        # self.customerList.currentTextChanged.connect(self.insertCustomer)
        # self.paragraphsList.currentTextChanged.connect(self.addParagraph)
        #self.setCentralWidget(dock)
        self.tabifyDockWidget(self.file_monitor, dock)
        b = QPushButton()
        b.setStyleSheet("""
        background-color:red;
        color:blue;
        """)
        dock.setTitleBarWidget(b)
        dock.setStyleSheet(
            """
             QFrame, QLabel, QToolTip {
border: 2px solid green;
border-radius: 4px;
padding: 2px;
background-image: url(images/welcome.png);
}
             height = 0;
    QMainWindow::separator  {
background: yellow;
width: 0px; /* when vertical */
height: 10px; /* when horizontal */
}

QMainWindow::separator:hover  {
background: red;
}
QGroupBox {
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                           stop: 0 #E0E0E0, stop: 1 #FFFFFF);
border: 2px solid gray;
border-radius: 5px;
margin-top: 1ex; /* leave space at the top for the title */
}

QGroupBox::title {
subcontrol-origin: margin;
subcontrol-position: top center; /* position at the top center */
padding: 0 3px;
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                           stop: 0 #FFOECE, stop: 1 #FFFFFF);
}

            """)

        self.setStyleSheet(
            """
             QFrame, QLabel, QToolTip {
     border: 2px solid green;
     border-radius: 4px;
     padding: 2px;
     background-image: url(images/welcome.png);
 }
            QMainWindow::separator { background-color: red; width: 5px; height: px; }
 QGroupBox {
     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #E0E0E0, stop: 1 #FFFFFF);
     border: 2px solid gray;
     border-radius: 5px;
     margin-top: 1ex; /* leave space at the top for the title */
 }

 QGroupBox::title {
     subcontrol-origin: margin;
     subcontrol-position: top center; /* position at the top center */
     padding: 0 3px;
     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #FFOECE, stop: 1 #FFFFFF);
 }


QTabBar
{
height:0px;
foreground-color:black;
background-color:yellow;
color:blue;
}
QTabBar::tab  {
    background: black;
    border: 2px solid #C4C4C3;
    border-bottom-color: #C2C7CB; /* same as the pane color */
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 2px;
}
            """)

    def setup_ui(self):
        self.setup_menus()
        self.setup_docks()
        self.setCentralWidget(QTextEdit(self))
        #self.setCentralWidget(self.file_monitor)
        t = self.tabifiedDockWidgets(self.file_monitor)
        print t


if __name__ == '__main__':
    # bench = Workbench()
    # print hasattr(bench, "editor")

    import sys

    app = QApplication(sys.argv)
    mainWin = Workbench()
    mainWin.show()
    sys.exit(app.exec_())