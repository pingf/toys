import sys
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import *
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = QsciScintilla()
    
    ## Choose a lexer
    ## This can be any Scintilla lexer, but the original example used Python
    lexer = QsciLexerPython(editor)
 
    ## Create an API for us to populate with our autocomplete terms
    api = Qsci.QsciAPIs(lexer)
    ## Add autocompletion strings
    api.add("aLongString")
    api.add("aLongerString")
    api.add("aDifferentString")
    api.add("sOmethingElse")
    ## Compile the api for use in the lexer
    api.prepare() 
    editor.setLexer(lexer)
 
    ## Set the length of the string before the editor tries to autocomplete
    ## In practise this would be higher than 1
    ## But its set lower here to make the autocompletion more obvious
    editor.setAutoCompletionThreshold(1)
    ## Tell the editor we are using a QsciAPI for the autocompletion
    
    
    editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)
     
    ## Render on screen
    editor.show() 
    ## Show this file in the editor
    editor.setText(open("autocomplete.py").read())
    sys.exit(app.exec_())
