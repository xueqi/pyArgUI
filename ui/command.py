'''
Created on May 10, 2017

@author: xueqi
'''

import logging

import widgets as _widgets
logger = logging.getLogger(__name__)

class CommandBox(_widgets.Listbox, object):
    def __init__(self, parent, **kwargs):
        super(CommandBox, self).__init__(parent, **kwargs)
        self.commands = []
        
        self.createActions()
        
    def addCommand(self, cmd):
        self.commands.append(cmd)
        self.insert(_widgets.END, cmd.name)
        
    def createActions(self):
        
        self.bind("<Double-Button-1>", self.doubleclick)
        print("action created")
    
    def doubleclick(self, event):
        logger.debug("Double clicked")
        print("double click %s" % self.curselection())
    
    def getCurrentModel(self):
        idx = self.curselection()
        if len(idx) >= 1:
            return self.commands[idx[0]]