'''
Created on May 11, 2017

@author: xueqi
'''
import os
# import Tkinter as _tk
import widgets as _widgets

WidgetTypeMap = {
    str : _widgets.LineEdit,
    float : _widgets.FloatField,
    int : _widgets.IntegerField,
    bool: _widgets.CheckBox, 
    
    }

class Argument(object):
    '''
        Argument created from Action object
    '''
    def __init__(self, action, defaultValue, widgetType = None, argType = str):
        self.name = action.dest
        self.action = action
        self.widgetType = widgetType
        self.argType = argType

        if self.widgetType is None:
            if argType in WidgetTypeMap:
                self.widgetType = WidgetTypeMap[argType]
            else:
                self.widgetType = _widgets.LineEdit
        elif type(self.widgetType) is str:
            if hasattr(_widgets, self.widgetType):
                        self.widgetType = getattr(_widgets, self.widgetType)
            else:
                self.widgetType = _widgets.LineEdit
        self.defaultValue = defaultValue
        if self.defaultValue == None:
            if self.argType is str:
                self.defaultValue = ""
            elif self.argType is bool:
                self.defaultValue = defaultValue
            elif self.argType is int:
                self.defaultValue = 0
            elif self.argType is float:
                self.defaultValue = 0.0
            
        self.widget = None
        self.label = None
        self.help = None
        
    def toWidget(self, parent, **kwargs):
        w = _widgets.Frame(parent, **kwargs)
        # add label
        lbl = _widgets.Label(parent, text = self.name)
        self.label = lbl
        wd = self.widgetType(parent, bg='green')
        if self.defaultValue is not None:
            wd.setValue(self.defaultValue)

        hlp = _widgets.Button(parent, text="?")
        hlp.bind("<Button-1>", self.showHelp)
        self.help = hlp
        self.widget = wd
        return w
    
    def showHelp(self, event):
        button = event.widget
        _widgets.showMessageBox("Help", "%s" % self.action.help)
    
    def getValue(self):
        if self.widget is not None: return self.widget.getValue()
        else: return None
    
    def valueChanged(self):
        print self.getValue(), self.defaultValue
        return self.getValue() != self.defaultValue
    
class CommandModel(object):
    '''
Command Model. 
instance variable:
    cmdPath: Command path
    parser: The parser loaded from cmdPath
    
'''
    def __init__(self, cmdPath):
        self.cmdPath = cmdPath
        self._parser = None
        self._name = None
        self.arguments = {}
    @property
    def parser(self):
        if self._parser is None:
            import imp
            md = imp.load_source("_md", self.cmdPath)
            setup_arg_parser = getattr(md, "setup_arg_parser")
            self._parser = setup_arg_parser()
        
        return self._parser
     
    @property
    def name(self):
        if self._name is None:
            self._name = os.path.basename(self.cmdPath)
        return self._name

    def getWidgetGroups(self):
        group = {}
        group['test'] = {
            }
        for action in self.parser.options.values():
            argType = action.type
            if argType is None:
                if action.default is False or action.default is True:
                    argType = bool
            widgetType = None
            
            if action.dest in self.parser._widgets:
                widgetType = self.parser._widgets[action.dest]
            arg = Argument(action, action.default, widgetType = widgetType, argType = argType)

            group['test'][arg.name] = arg
            self.arguments[arg.name] = arg
        return group
    
    def run(self, stdout = None, stderr= None):
        ''' TODO: Move to a controller
        '''        
        # need to rebuild command line
        
        import subprocess
        cmdList = [self.cmdPath]
        for arg in self.arguments.values():
            print arg.name
            if arg.valueChanged():
                action = arg.action
                if action.option_strings:
                    cmdList.append(action.option_strings[0])
                if arg.argType is not bool:
                    cmdList.append("%s" % arg.getValue())
        p = subprocess.Popen(cmdList, stdout = subprocess.PIPE, 
                             stderr = subprocess.PIPE)

        def asyncRead(p, ):
            stdoutDone = False
            stderrDone = False
            while not stdoutDone or not stderrDone:
                if not stdoutDone:
                    line = p.stdout.readline()
                    
                    # wired behavior
                    if len(line) == 0 or line == "None\n":
                        stdoutDone = True
                if not stderrDone:
                    line = p.stderr.readline()
                    if not line:
                        stderrDone = True