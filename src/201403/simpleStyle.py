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
        self.styles = {0:'red',1:'green'}
    def description(self, style):
        return self.styles.get(style, '')
        
    def color(self, style):
        if style == 0:
            return QColor('#00FFAA')
        elif style == 1:
            return QColor('#FF00AA') 
        return QsciLexerCustom.defaultColor(self, style)
    def font(self, style):
        font=QsciLexerCustom.defaultFont(self,style)
        if style == 0:
            font.setBold(True)
        elif style == 1:
            font.setItalic(True)
            font.setUnderline(True)
            font.setPointSize(16) 
        return font

    def paper(self, style): 
        if style == 0:
            return QColor('#FF00AA')
        elif style == 1:
            return QColor('#00FFAA')
        return QsciLexerCustom.defaultPaper(self, style)    
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