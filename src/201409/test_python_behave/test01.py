class TextEditor:
    def __init__(self,text):
        self.text=text
        self.cursorPos=0
    def get_text(self):
        return self.text
    def prev_word(self,pos):
        text=self.text
        while text[pos]==' ':
            pos-=1
        end=pos+1
        while text[pos]!=' ':
            pos-=1
        begin=pos+1
        return text[begin:end]
        
    