'''
Created on May 11, 2017

@author: xueqi
'''
import Tkinter as _tk

import widgets as _widgets
from ui.cmdmodel import CommandModel
from ui.program import ProgramWindow
import cmd

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
        cmdListPanel = _tk.Frame(parent, bg = "cyan")
        cmdListPanel.grid(row=0, column = 0, sticky = _tk.N + _tk.S + _tk.W + _tk.E)
        lbl = _tk.Label(cmdListPanel, text = "Commands")
        lbl.pack(side = _tk.TOP)
        # command selection
        from ui.command import CommandBox
        cmdbox = CommandBox(cmdListPanel)
        cmdbox.bind("<ButtonRelease-1>", self.showProgram)
        cmdbox.pack(side= _tk.TOP, expand=True, fill = _tk.BOTH)
        self.cmdListBox = cmdbox
        
        # the program panel
        progPanel = _tk.Frame(parent, width = "400", height = "400", bg = "green")
        progWindow = ProgramWindow(progPanel, bg="red")
        progWindow.pack(fill=_tk.BOTH, expand = True)
        self.programWindow = progWindow
        progPanel.grid(row=0, column = 1, sticky = _tk.N + _tk.S + _tk.W + _tk.E)

        parent.grid_rowconfigure(0, weight = 1)
        
        logPanel = _widgets.TabPanel(parent, bg="purple")
        logPanel.grid(row=1, column = 1, sticky = _tk.N + _tk.S + _tk.W + _tk.E)
        
        self.errorlog = _widgets.StreamTextView(logPanel, height = "100")
        logPanel.addTab("error", self.errorlog)
        
        self.outputlog = _widgets.StreamTextView(logPanel, height = "100")
        logPanel.addTab("output", self.outputlog)
        
        logPanel.setCurrentTab(0)
        
    def showProgram(self, event):
        cmdbox = event.widget
        cmdModel = cmdbox.getCurrentModel()
        self.programWindow.command = cmdModel
        self.programWindow.setStdout(self.outputlog)
        self.programWindow.setStderr(self.errorlog)
    
    def addCommand(self, cmdPath):
        cmm = CommandModel(cmdPath)
        self.cmdListBox.addCommand(cmm)
    
        
class MyApp(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def run(self):
        import os
        root = _tk.Tk()
        root.deiconify()
        root.withdraw()
        w = MyMainWindow(root, width = 800, height = 600)
        w.isMasterWindow = True
        w.pack_propagate(False)
        w.geometry("800x600")
        #w.resizable(width=False, height = False)
        cmds = ['cf_init_project', 'cf_ctf', 'cf_init_frealign']
        cmdDir = "/home/xueqi/py_cf_mt/commands/"
        for cmd in cmds:
            w.addCommand(os.path.join(cmdDir, cmd))
        
        root.wm_title("root")
        w.wm_title("MainWindow")
        root.mainloop()
        
if __name__ == "__main__":
    import sys
    MyApp(sys.argv).run()
        