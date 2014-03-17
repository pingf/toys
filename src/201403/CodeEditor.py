'''
Created on Mar 1, 2014

@author: jesse
'''


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *
import os.path as path

class CodeEditor(QsciScintilla):
    def __init__(self, filename='untitled'):
        super(CodeEditor, self).__init__()
        self.setUtf8(True) # use utf8
        
        self.filename = filename
        if filename.find("./"):
            filename = path.abspath(filename)
        slash_pos = filename.rfind("/")
        if slash_pos == -1:
            self.nickname = filename
        else:
            self.nickname = filename[slash_pos+1:]
    
        self.open(filename)

    def set_filename(self, filename):
        self.filename = filename

    def current_filename(self):
        return self.filename

    def keyPressEvent(self, event):
        key = event.key()
        modifier = event.modifiers()
        if key == Qt.Key_S and modifier & Qt.ControlModifier:
            self.save()
        return super(CodeEditor, self).keyPressEvent(event)

 

    def read_text(self, in_file):
        text = None
        if in_file.open(QFile.ReadOnly | QFile.Text):
            text = in_file.readAll()
            try:
                text = str(text, encoding='utf-8')
            except TypeError:
                text = str(text)
        return text

    def open(self, filename): 
        if not filename:
            self.setText("")
            return False
        in_file = QFile(filename) 
        text = self.read_text(in_file)
        if text is not None:
            self.setText(text) 
            in_file.close()
            return True
        in_file.close()
        return False

    def save(self):
        self.save_as(self.filename)

    def save_as(self, filename=None):
        if filename is not None:
            out_file = QFile(filename)
            if out_file.open(QFile.WriteOnly | QFile.Text):
                out_file.writeData(self.text())
                out_file.close()
                self.current_filepath = filename
                return True
        return False
    
    
if __name__ == '__main__': 
    import sys 
    app = QApplication(sys.argv)
    mainWin = CodeEditor('../text')
    mainWin.show()
    sys.exit(app.exec_())