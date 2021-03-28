# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 19:23:21 2021

@author: Stephan

This is an example on how to use the PSData.py file
"""
import PSData as PS

# just paste the file source here:
simpleData = PS.jparse([r'filelocation\A.pssession',r'filelocation\B.pssession'])

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
import PSDataPlot as PSP # this is optional. Only for using the plot functionality I build.

# pass the simpleData to the plotting object
plot = PSP.PSPlot(simpleData)
#plot.groups = {'G1':{'SWV 1','SWV 2'},'G2':{'SWV 3', 'SWV 4'},'G3':{'CV 1'},'G4':{'CV 2'}}
#plot.groups = {'G1':{'EIS 1','EIS 2'},'G2':{'EIS 3','EIS 4'}}
#plot.baseline.startPosition = 3
#plot.baseline.endPosition = 50
#plot.methodFilter = 'SWV'
#plot.splitGraphs = True
#plot.titles = ['SWV','CV']
plot.show()
