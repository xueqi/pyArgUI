"""
    decorator tutorial : 
    @see <a href="http://www.artima.com/weblogs/viewpost.jsp?thread=240845">Python Decorators II: Decorator Arguments</a>
"""
import os, sys
import textwrap
import collections as _collections

try:
    from gooey import Gooey, GooeyParser
    
    def ChuffGooey(f=None, *gooey_args, **gooey_kwargs):
        '''
            ChuffGooey is intended to call Gooey UI if no argument supplied in command line. 
        '''
        # this is the actual decorator to run function without gooey
        def gooey_wrapper(f1):
            def default_wrapper(*args, **kwargs):
                return f1(*args, **kwargs)
            default_wrapper.__name__ = f1.__name__
            return default_wrapper
        def gooey_wrapper_no_args(*args, **kwargs):
            return f(*args, **kwargs)
        if len(sys.argv) > 1:
            # ignore-gooey is added when calling function from the gooey interface. So if we want to run function without interface, we have to remove the --ignore-gooey
            if '--ignore-gooey' in sys.argv:
                sys.argv.remove('--ignore-gooey')
            if f is None:
                return gooey_wrapper
            else:
                return gooey_wrapper_no_args
        # if there is no options supplied , we just return the gooey decorator
        return Gooey(f, *gooey_args, **gooey_kwargs)
    Parser = GooeyParser
except:
    print "Warning: No Gooey module found or Gooey can not import."
    print "Fall to command line"
    import argparse
    Parser = argparse.ArgumentParser

    # decorator do nothing. This is mainly for compatibility for old Gooey code
    
    def ChuffGooey(*gooey_args, **gooey_kwargs):
        def wrapper(f1):
            def func_wrapper(*args, **kwargs):
                return f1(*args, **kwargs)
            return func_wrapper
        if len(gooey_args) > 0 and callable(gooey_args[0]):
            return wrapper(gooey_args[0])
        else:
            return wrapper

class _ArgumentGroup(argparse._ArgumentGroup):
    def __init__(self, *args, **kwargs):
        super(_ArgumentGroup, self).__init__(*args, **kwargs)
        self.options = _collections.OrderedDict()
        self._widgets = {}
    def add_argument(self, *args, **kwargs):
        widget = kwargs.get('widget', None)
        if not hasattr(self, 'widgets'):  # this detect if class is GooeyParser
            kwargs.pop('widget', None)
            
        if 'help' in kwargs: kwargs['help'] = textwrap.fill(kwargs['help'], 35)
        
        action = super(_ArgumentGroup, self).add_argument(*args, **kwargs)
        
        # add to widgets
        if action.dest != "help":
            self.options[action.dest] = action
            if widget is not None:
                self._widgets[action.dest] = widget
        
        return action

class ChuffParser(Parser):
    '''
        ChuffParser. Wrapper of argparse.ArgumentParser or GooeyParser
    '''
    def __init__(self, **kwargs):
        kwargs['fromfile_prefix_chars'] = '@'
        self.options = _collections.OrderedDict()
        self._widgets = {}
        self._groups = []
        super(ChuffParser, self).__init__(**kwargs)
    
    def add_argument(self, *args, **kwargs):
        widget = kwargs.get('widget', None)
        if not hasattr(self, 'widgets'):  # this detect if class is GooeyParser
            kwargs.pop('widget', None)
            
        if 'help' in kwargs: kwargs['help'] = textwrap.fill(kwargs['help'], 35)
        
        action = super(ChuffParser, self).add_argument(*args, **kwargs)
        
        # add to widgets
        if action.dest != "help":
            self.options[action.dest] = action
            if widget is not None:
                self._widgets[action.dest] = widget
        
        return action
    
    def parse_args(self, *args, **kwargs):
        if self.description is None: self.description = ''
        self.description += ("\nCurrent working directory: \n%s" % os.getcwd())
        return super(ChuffParser, self).parse_args(*args, **kwargs)
    
    def add_argument_group(self, *args, **kwargs):
        group = _ArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        self._groups.append(group)
        return group
        
    