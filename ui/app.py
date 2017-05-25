'''
Created on May 11, 2017

@author: xueqi
'''
import Tkinter as _tk

import widgets as _widgets
from ui.cmdmodel import CommandModel
from ui.program import ProgramWindow

class MyMainWindow(_widgets.mainwindow.AppWindow):
    def __init__(self, parent, *args, **kwargs):
        self.cmdListBox = None
        self.programWindow = None
        super(MyMainWindow, self).__init__(parent, *args, **kwargs)
        
    def buildMainWindow(self, parent = None):
        parent = parent or self
        parent.grid_columnconfigure(1, weight = 1)
        parent.grid_rowconfigure(0, minsize=400)
        parent.grid_rowconfigure(1, minsize=100)
        cmdListPanel = _tk.Frame(parent)
        cmdListPanel.grid(row=0, column = 0, sticky = _tk.N + _tk.S + _tk.W + _tk.E)
        lbl = _tk.Label(cmdListPanel, text = "Commands")
        lbl.pack(side = _tk.TOP)
        # command selection
        from ui.command import CommandBox
        cmdbox = CommandBox(cmdListPanel)
        cmdbox.bind("<Double-Button-1>", self.showProgram)
        cmdbox.pack(side= _tk.TOP, expand=True, fill = _tk.BOTH)
        self.cmdListBox = cmdbox
        
        # the program panel
        progPanel = _widgets.Frame(parent, bg = "green")
        progWindow = ProgramWindow(progPanel, bd = 2, bg = 'gray', relief = _tk.SOLID)
        progWindow.pack(fill=_tk.BOTH, expand = True, in_ = progPanel)
        self.programWindow = progWindow
        progPanel.grid(row=0, column = 1, sticky = _tk.N + _tk.S + _tk.W + _tk.E)

        parent.grid_rowconfigure(0, weight = 1)
        
        logPanel = _widgets.TabPanel(parent)
        logPanel.grid(row=1, column = 1, sticky = _tk.N + _tk.S + _tk.W + _tk.E)

        self.outputlog = _widgets.StreamTextView(logPanel, bg = "gray")
        logPanel.add(self.outputlog, text = "Output")
        
        self.errorlog = _widgets.StreamTextView(logPanel, bg = "red")
        logPanel.add(self.errorlog, text = "Error")
                
        logPanel.select(0)
        
    def showProgram(self, event):
        cmdbox = event.widget
        cmdModel = cmdbox.getCurrentModel()
        self.programWindow.command = cmdModel
        
        self.programWindow.setStdout(self.outputlog)
        self.programWindow.setStderr(self.errorlog)
    
    def addCommand(self, cmdPath):
        cmm = CommandModel(cmdPath)
        self.cmdListBox.addCommand(cmm)
    
        

        
if __name__ == "__main__":
    import sys
    # MyApp(sys.argv).run()
        