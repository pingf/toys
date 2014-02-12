'''
Created on Feb 11, 2014

@author: Jesse MENG
'''
import  sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FakeShell(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(900)
        self.setMinimumHeight(400)
        self.process = QProcess(self)

        self.terminal = QTextBrowser() 
        self.buttons=[QPushButton('ls',self),
                      QPushButton('gdb',self),
                      QPushButton('help',self),
                      QPushButton('quit',self)]
        
        buttonLayoutH = QHBoxLayout()
        for i,b in enumerate(self.buttons): 
            b.clicked.connect(getattr(self,'button'+str(i)+'Clicked'))
            buttonLayoutH.addWidget(b)

        layout = QVBoxLayout(self)
        layout.addLayout(buttonLayoutH)
        layout.addWidget(self.terminal) 

        self.process.setProcessChannelMode(QProcess.MergedChannels) 
        self.process.readyRead.connect(self.showAll)  
        self.process.start('bash', ['-i'], mode=QIODevice.ReadWrite)
        
    def showOut(self, output):
        output_split = output.split("\n")
        for i in output_split[:]:
            if len(i) > 0: 
                self.terminal.append(str(i)) 
                self.terminal.moveCursor(QTextCursor.End)
        
    def showAll(self):  
        self.process.waitForReadyRead(msecs=50)
        output = self.process.readAllStandardOutput() 
        self.showOut(output)

    def button0Clicked(self):
        self.process.writeData('ls\n')
    def button1Clicked(self): 
        self.process.writeData('gdb\n')
    def button2Clicked(self):
        self.process.writeData('help\n')
    def button3Clicked(self):
        self.process.writeData('quit\n')
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = FakeShell()
    main.show()
    sys.exit(app.exec_())