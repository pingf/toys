'''
Created on Mar 11, 2014

@author: jesse
'''
from CodeEditor import *
from PyQt4.Qsci import *
class Completer(QListView): 
    def __init__(self,editor):
        super(Completer,self).__init__()
        self.editor=editor
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.setWindowOpacity(0.8) 
        self.freq_map={}
    def append(self,s):
        if self.freq_map.has_key(s):
            return
        self.freq_map[s]=0
        item = QStandardItem(s)
        self.model.appendRow(item)  
    def keyPressEvent(self,event):
        
        if event.key() == Qt.Key_Escape:
            self.close()
        
        if event.key() == Qt.Key_Return: 
            s=(self.currentIndex().data().toString())
	    print s
            p=self.editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS) 
            self.editor.SendScintilla(QsciScintilla.SCI_INSERTTEXT,p,str(s))
            self.editor.SendScintilla(QsciScintilla.SCI_GOTOPOS,p+len(s))
            
            self.freq_map[str(s)]+=1 
            self.close()
            
        super(Completer,self).keyPressEvent(event)
 
 
class DeEditor(CodeEditor):
    def __init__(self,name='untitled'):
        super(DeEditor,self).__init__(name)
        
        self.font = QFont()
        
        self.font.setFamily('Microsoft Yahei Mono')
        self.font.setFixedPitch(True)
        self.font.setPointSize(12)
        self.setFont(self.font)
        
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6) 
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))
        self.setIndentationWidth(4)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        lexer = DeLexer(self)
        lexer.setDefaultFont(QFont('Courier'))
        self.setLexer(lexer) 
        self.cp = Completer(self)
    def keyPressEvent(self,event):  
        if event.key() == Qt.Key_Escape:
            self.cp.setGeometry(QRect(100, 100, 400, 200))
            for s in self.lexer().ws:
                self.cp.append(s)
            self.cp.show()
            pos = self.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
            x,y = (self.SendScintilla(QsciScintilla.SCI_POINTXFROMPOSITION, 0, pos),
                    self.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, pos))
 
            self.cp.move(self.mapToGlobal(QPoint(x,y))) 
        super(DeEditor,self).keyPressEvent(event)
    def closeEvent(self, *args, **kwargs):
        self.cp.close()
        return CodeEditor.closeEvent(self, *args, **kwargs)
 
class DeLexer(QsciLexerCustom):
    def __init__(self, parent=None):
        super(DeLexer,self).__init__(parent) 
        self.styles = {0:'defualt',1:'highlight'}
        self.ws=set()
    def description(self, style):
        return self.styles.get(style, '')
        
    def color(self, style):
        if style == 1: return QColor('#3366FF')
        return QsciLexerCustom.defaultColor(self, style)
    def font(self, style):
        font=QsciLexerCustom.defaultFont(self,style)
        if style == 1:
            font.setItalic(True)
            font.setUnderline(True)
            font.setPointSize(16) 
        return self.parent().font
    def styleText(self, start, end): 
        editor = self.editor()          
    
        source = bytearray(end-start)
        editor.SendScintilla(QsciScintilla.SCI_GETTEXTRANGE, start,end, source)
        
        index = editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, start) 
         
        for i,line in enumerate(source.splitlines(True)):
            line_len = len(line)
            func_pos = line.find("function")
            brac_pos = line.find("(") 
            pos = editor.SendScintilla(QsciScintilla.SCI_GETLINEENDPOSITION, index)-line_len+1
            if func_pos>-1 and brac_pos>-1:
                func_name = line[func_pos+8:brac_pos].strip() 
                 
                self.ws.add(str(func_name))
                self.startStyling(func_pos+pos+8,0x1f)
                self.setStyling(brac_pos-func_pos-8,1) 
            index+=1 
 

if __name__ == '__main__': 
    import sys 
    app = QApplication(sys.argv)
    mainWin = DeEditor("test.de")
    mainWin.show()
    sys.exit(app.exec_())
