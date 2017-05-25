'''
Created on May 10, 2017

@author: xueqi
'''
import unittest
import os


class Test(unittest.TestCase):


    def testMain(self):
        mw = MyApp()
        mw.run()
 
class MyApp(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def run(self):
        from ui.app import MyMainWindow
        import Tkinter as _tk
        root = _tk.Tk()
        root.deiconify()
        root.withdraw()
        w = MyMainWindow(root, width = 800, height = 600)
        w.isMasterWindow = True
        w.pack_propagate(False)
        w.geometry("800x600")
        #w.resizable(width=False, height = False)
        cmds = ['cf_init_project', 'cf_import_micrographs', 'cf_ctf', 'cf_ref_align_mt.py', 'cf_init_frealign']
        cmdDir = "/Users/xueqi/dev/tk/py_cf_mt/commands/"
        import chuff_parser
        print chuff_parser
        for cmd in cmds:
            w.addCommand(os.path.join(cmdDir, cmd))
        
        root.wm_title("root")
        w.wm_title("MainWindow")
        root.mainloop()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
    app = MyApp()
    app.run()