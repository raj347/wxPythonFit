
# see the included wxThreadExample.py file

import os, sys, time, threading
import wx
from . import CustomEvents

# ensure pyeq3 can be imported
if -1 != sys.path[0].find('pyeq3-master'):raise Exception('Please rename git checkout directory from "pyeq3-master" to "pyeq3"')
exampleFileDirectory = sys.path[0][:sys.path[0].rfind(os.sep)]
pyeq3IimportDirectory =  os.path.join(os.path.join(exampleFileDirectory, '..'), '..')
if pyeq3IimportDirectory not in sys.path:
    sys.path.append(pyeq3IimportDirectory)
    
import pyeq3


class FittingThread(threading.Thread):
    def __init__(self, notify_window, equation):
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self.equation = equation
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()


    def run(self):

        statusString = 'Fitting data...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.Solve()
    
        statusString = 'Calculating model errors...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.CalculateModelErrors(self.equation.solvedCoefficients, self.equation.dataCache.allDataCacheDictionary)
    
        statusString = 'Calculating coefficient and fit statistics...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.CalculateCoefficientAndFitStatistics()

        statusString = 'Creating reports...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
            
        # the fitted equation is now the event data, not a status update string
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(self.equation))
