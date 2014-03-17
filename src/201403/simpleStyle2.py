'''
Created on Mar 1, 2014

@author: jesse
'''


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *

class CodeEditor(QsciScintilla):
    def __init__(self, filename='untitled'):
        super(CodeEditor, self).__init__()
        self.setUtf8(True) # use utf8
        
        self.filename = filename
        self.open(filename)
        self.lexer = Lexer(self)
        self.setLexer(self.lexer)
        
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
 
class Lexer(QsciLexerCustom):
    def __init__(self, parent):
        super(Lexer,self).__init__(parent)
        #QsciLexerCustom.__init__(self, parent)
        self.styles = [
          QsciStyle(0, QString("base"), QColor("#000000"), QColor("#ffffff"), QFont('Courier',10), False),
          QsciStyle(1, QString("comment"), QColor("#008000"), QColor("#eeffee"), QFont('Courier',20), False),
        ]
    def description(self, style): 
        for i in self.styles: 
            if i.style() == style: 
                s=i.description()
                return s
        return "default"
        
    def color(self, style):
        for i in self.styles: 
            if i.style() == style:  
                return i.color()
        return QsciLexerCustom.defaultColor(self, style)
    def font(self, style): 
        for i in self.styles: 
            if i.style() == style:  
                return i.font()
        return QsciLexerCustom.defaultFont(self,style)

    def paper(self, style): 
        
        for i in self.styles: 
            if i.style() == style:  
                return i.paper()
        return QsciLexerCustom.defaultColor(self, style) 
    def eolFill(self, style):
        return True 
 
    def styleText(self, start, end):
        editor = self.editor()          

        source = ''
        text_len=editor.length()
           
        source = bytearray(text_len)
        editor.SendScintilla(QsciScintilla.SCI_GETTEXTRANGE, 0,text_len, source)
        
      
        self.startStyling(0, 0x1f)
        for i,line in enumerate(source.splitlines(True)):
            line_len = len(line)
            if i%2==0:
                self.setStyling(line_len,0)
            else:
                self.setStyling(line_len,1)
          
if __name__ == '__main__': 
    import sys 
    app = QApplication(sys.argv)
    mainWin = CodeEditor('text')
    mainWin.show()
    sys.exit(app.exec_())