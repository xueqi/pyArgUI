'''
Created on May 10, 2017

@author: xueqi
'''
import unittest
import os

class Test(unittest.TestCase):


    def testMain(self):
        from ui.command import MainWindow
        mw = MainWindow(os.path.join("..", "ui/xmls/app.xml"))
        mw.run()
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()