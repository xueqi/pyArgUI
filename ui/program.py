'''
Created on May 11, 2017

@author: xueqi
'''
import Tkinter as _tk
import widgets as _widgets
class ProgramWindow(_tk.Frame, object): 
    '''
    The program window to show the program inputs
    '''
    
    def __init__(self, parent, **kwargs):
        '''
        Constructor
        '''
        super(ProgramWindow, self).__init__(parent, **kwargs)
        self._command = None
        self._frame = None
        
        self._stdout = []
        self._stderr = []
        if "stdout" in kwargs:
            stdout = kwargs["stdout"]
            if type(stdout) is list or type(stdout) is tuple:
                self._stdout.extend(stdout)
            else:
                self._stdout.append(stdout)        
        if "stderr" in kwargs:
            stderr = kwargs["stderr"]
            if type(stderr) is list or type(stderr) is tuple:
                self._stderr.extend(stderr)
            else:
                self._stderr.append(stderr)
        # contains the widgets for the parameters, which is used to populate the value        
        self.widgets = {} 
    
    def setStdout(self, stdout):
        if stdout not in self._stdout:
            self._stdout.append(stdout)
    def setStderr(self, stderr):
        if stderr not in self._stderr:
            self._stderr.append(stderr)
            
    def buildUI(self):
        if not self._command: return
        if self._frame is not None:
            self._frame.destroy()
        self._frame = _widgets.ScrollFrame(self)
        # Title
        label = _tk.Label(self._frame, text = self._command.name, bg = "powder blue")
        label.pack(side=_tk.TOP, fill = _tk.X)
        
        # use model to build the window
        
        for groupName, widgetGroup in self._command.getWidgetGroups().items():
            groupWidget = _tk.Frame(self._frame)
            groupWidget.pack(side=_tk.TOP, fill = _tk.BOTH)
            groupTitle = _tk.Label(groupWidget, text = groupName,
                                   bg = "gray", justify = _tk.LEFT) #, relief = _tk.RAISED)
            groupTitle.pack(side=_tk.TOP, fill = _tk.X,
                             expand = False)
            groupWidgetArea = _tk.Frame(groupWidget)
            groupWidgetArea.pack(side = _tk.TOP, fill = _tk.BOTH)
            # The widgets
            i = 0
            groupWidgetArea.grid_columnconfigure(0, weight = 1)
            groupWidgetArea.grid_columnconfigure(1, weight = 1)
            for arg in widgetGroup.values():
                w = arg.toWidget(groupWidgetArea)
                arg.label.grid(row=i, column = 0, sticky = _tk.E, in_ = groupWidgetArea)
                arg.widget.grid(row=i, column = 1, sticky = _tk.E + _tk.W, in_ = groupWidgetArea)
                arg.help.grid(row=i, column = 2, in_ = groupWidgetArea)
                self.widgets[arg.name] = arg.widget
                i += 1
        
        # add run button
        buttonGroup = _tk.Frame(self._frame)
        buttonGroup.pack(fill=_tk.X)
        runButton = _tk.Button(self._frame, text = "Run")
        runButton.pack(in_ = buttonGroup)
        runButton.bind("<Button-1>", self.runCommand)
        self._frame.pack(fill = _tk.BOTH, expand = True)
        self._frame.update()
        self._frame.update_idletasks()
        
    def runCommand(self, event = None):

        # run command
        import sys
        self.outputlog = sys.stdout
        self.errorlog = sys.stderr
        if len(self._stdout) > 0: 
            self.outputlog = self._stdout[0]
        if len(self._stderr) > 0:
            self.errorlog = self._stderr[0]
        self._command.run(stdouts = self.outputlog, stderrs = self.errorlog)
    @property
    def command(self):
        return self._command
    
    @command.setter
    def command(self, value):
        self._command = value

        self.buildUI()

#     