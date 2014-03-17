'''
Created on Mar 1, 2014

@author: jesse
'''


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qsci import *

class CodeEditor(QsciScintilla):
    def __init__(self, filename='untitled',parent=None):
        super(CodeEditor, self).__init__(parent)
        self.setUtf8(True) # use utf8
        
        #self.editor = parent
        self.mw = parent

        self.title = None
        self.docid = None

        self._filepath = None # not None for external file

        self.setup()

    def setup(self):
        self.setup_font()
        self.setup_margin0()
        self.setup_margin1()
        self.setup_cursor()
        self.setup_lexer()
        self.setup_custom()

    def setup_custom(self):
        pass

    def setup_font(self):
        # Set the default font
        fontsize = 16
        font = QFont()
        font.setFamily('Courier')
        font.setBold(True)
        font.setFixedPitch(True)
        font.setPointSize(fontsize)
        self._font = font
        self.setFont(font)
        self.setMarginsFont(font)

    def setup_margin0(self):
        # Margin 0 is used for line numbers
        settings = QSettings()
        numbers = settings.value('editor/linenumbers', True, bool)
        if numbers:
            self.show_line_numbers()
        else:
            self.hide_line_numbers()
        self.setMarginsBackgroundColor(QColor("#444444"))
        self.setMarginsForegroundColor(QColor('#999999'))

    def setup_margin1(self):
        # Disable 2nd margin (line markers)
        self.setMarginWidth(1, 0)

        # Match parentheses
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setUnmatchedBraceBackgroundColor(QColor('#000000'))
        self.setUnmatchedBraceForegroundColor(QColor('#FF4444'))
        self.setMatchedBraceBackgroundColor(QColor('#000000'))
        self.setMatchedBraceForegroundColor(QColor('#44FF44'))

    def setup_cursor(self):
        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretForegroundColor(QColor('#8888FF'))
        self.setCaretLineBackgroundColor(QColor("#222222"))

    def setup_lexer(self):
        # Set Python lexer
        lexer = QsciLexerPython(self)
        lexer.setDefaultFont(self._font)
        self.setLexer(lexer)
        lexer.setDefaultPaper(QColor("#000000"))
        lexer.setPaper(QColor("#000000"))
        lexer.setAutoIndentStyle(QsciScintilla.AiOpening)
        self.setstyle()

        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)
        self.setIndentationWidth(4)

    def hide_line_numbers(self):
        self.setMarginWidth(0, 0)

    def show_line_numbers(self):
        fontmetrics = QFontMetrics(self._font)
        self.setMarginWidth(0, fontmetrics.width("00") + 6)
        self.setMarginLineNumbers(0, True)

    def wrap(self):
        self.setWrapMode(QsciScintilla.SC_WRAP_WORD)
    def nowrap(self):
        self.setWrapMode(QsciScintilla.SC_WRAP_NONE)

    def setstyle(self):
        styles = dict(Default = 0, Comment = 1, Number = 2,
                    DoubleQuotedString = 3, SingleQuotedString = 4,
                    Keyword = 5,TripleSingleQuotedString = 6,
                    TripleDoubleQuotedString = 7, ClassName = 8,
                    FunctionMethodName = 9, Operator = 10,
                    Identifier = 11, CommentBlock = 12,
                    UnclosedString = 13, HighlightedIdentifier = 14,
                    Decorator = 15)

        style = dict(Default = '#FFFFFF',
                        Comment = '#9999FF',
                        Identifier = '#CCFF99',
                        SingleQuotedString = '#FF6666',
                        DoubleQuotedString = '#FF6666',
                        TripleSingleQuotedString = '#FF6666',
                        TripleDoubleQuotedString = '#FF6666',
                        FunctionMethodName = '#77DDFF',
                        ClassName = '#CC44FF',
                        Number = '#44FFBB',

                        )

        lexer = self.lexer()
        for k in styles.keys():
            colorname = style.get(k, '#FFFFFF')
            color = QColor(colorname)
            n = styles[k]
            lexer.setColor(color, n)
            lexer.setFont(self._font)

    def keyPressEvent(self, ev):
        k = ev.key()
        mdf = ev.modifiers()

        Return = Qt.Key_Return
        Control = Qt.ControlModifier
        Shift = Qt.ShiftModifier
        Slash = Qt.Key_Slash
        Question = Qt.Key_Question
        Minus = Qt.Key_Minus
        V = Qt.Key_V
        Z = Qt.Key_Z

        passthru = True

        lead = 0
        if k == Return:
            lineno, linedex = self.getCursorPosition()
            line = str(self.text(lineno)).strip()
            indent = self.indentation(lineno)
            char = line[-1:]
            colon = ':'
            if char == colon:
                # auto indent
                indent += 4
            QsciScintilla.keyPressEvent(self, ev)
            self.insert(' '*indent)
            self.setCursorPosition(lineno+1, indent)
            passthru = False

        elif mdf & Control and k==Slash:
            self.commentlines()
            passthru = False

        elif mdf & Control and k==Question:
            self.commentlines(un=True)
            passthru = False

        elif mdf & Control and k==Minus:
            self.editor.zoomout()
            passthru = False

        elif mdf & Control and k==V:
            self.paste()
            passthru = False

        elif mdf & Control and mdf & Shift and k==Z:
            self.redo()
            passthru = False

        if passthru:
            QsciScintilla.keyPressEvent(self, ev)

        #self.editor.settitle()
        self.update_window_modified()

    def update_window_modified(self):
        pass
        #self.mw.show_modified_status()

    def commentlines(self, un=False):
        if self.hasSelectedText():
            linenostart, _, linenoend, _ = self.getSelection()
        else:
            linenostart, _ = self.getCursorPosition()
            linenoend = linenostart + 1

        for lineno in range(linenostart, linenoend):
            line = self.text(lineno)
            if line and not line.isspace():
                indent = self.indentation(lineno)
                if not un:
                    self.insertAt('#', lineno, indent)
                elif line[indent] == '#':
                    self.setSelection(lineno, indent, lineno, indent+1)
                    self.replaceSelectedText('')

    def paste(self):
        clipboard = QtGui.QApplication.clipboard()
        txt = clipboard.text()
        md = clipboard.mimeData()
        logger.info(md)

        newtxt = []
        for line in txt.split('\n'):
            line = str(line)
            if line.startswith('>>> ') or line.startswith('... '):
                line = line[4:]
            newtxt.append(line)
        txt = '\n'.join(newtxt)

        self.insert(txt)

    def contextMenuEvent(self, ev):
        '''Switch Redo to Ctrl-Shift-Z

        Connection of actual typed shortcut is in keyPressEvent()
        '''
        print '1'

        menu = self.createStandardContextMenu()
        actions = menu.actions()
        redo = actions[1]
        sep0 = actions[2]

        menu.removeAction(redo)
        redoaction = QAction('Redo111', menu)
        redoshortcut = QKeySequence(Qt.CTRL +
                                            Qt.SHIFT +
                                            Qt.Key_Z)
        redoaction.setShortcut(redoshortcut)
        redoaction.triggered.connect(self.redo)
        if not self.isRedoAvailable():
            redoaction.setDisabled(True)
        menu.insertAction(sep0, redoaction)

        menu.exec_(ev.globalPos())

        
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

if __name__ == '__main__': 
    import sys 
    app = QApplication(sys.argv)
    mainWin = CodeEditor('text')
    mainWin.show()
    sys.exit(app.exec_())