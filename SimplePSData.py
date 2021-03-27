# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 19:23:21 2021

@author: Stephan

This is an example on how to use the PSData.py file
"""
import PSData as PS

# just paste the file source here:
simpleData = PS.jparse([r'filelocation\A.pssession', r'filelocation\E.pssession'])

# and then you can access the experiment list like this:
#print(simpleData.experimentList)

# you can find out in what file the experiment is located:
# simpleData.inFile('SWV 1')

""" SWV and CV """
# and you can access the data by using the data dictionary:
#print(simpleData.data['SWV 1'].xvalues)

# or you can use the experiment list to iterate through the experiments:
#for experiment in simpleData.experimentList:
#    print(simpleData.data[experiment].yvalues)
#    print(simpleData.data[experiment].xvalues)

""" EIS """
# EIS experiments have more information
# check out the class EISMeasurement for the different accessible components
# example:
#print(simpleData.data['EIS 1'].phase)

""" PS Plot """
#import PSDataPlot as PSP # this is optional. Only for using the plot functionality I build.

# pass the simpleData to the plotting object
#plot = PSP.PSPlot(simpleData)
#plot.baseline.startPosition = 5
#plot.baseline.endPosition = 50
#plot.methodFilter = 'SWV'
#plot.splitGraphs = True
#plot.titles = ['title_1','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
#plot.show()
