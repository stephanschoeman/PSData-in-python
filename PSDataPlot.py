# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 19:43:23 2021

@author: Stephan
"""

import matplotlib.pyplot as plt

class axis:
    __slots__ = ['xvalues','yvalues']
    
    def __init__(self):
        self.xvalues = []
        self.yvalues = []

class PSPlot:
    @property
    def titles(self):
        return self._titles
    
    @titles.setter
    def titles(self, val):
        self._titlesOn = True
        self._titles = val
    
    @property
    def methodFilter(self):
        return self._methodFilter
    
    @methodFilter.setter
    def methodFilter(self, val):
        self._filterOnMethod = True
        self._methodFilter = val
    
    @property
    def groups(self):
        return self._groups
        
    @groups.setter
    def groups(self, val):
        self._grouping = True
        self._groups = val
        
    def __init__(self, PSData):
        self._filterOnMethod = False
        self._PlotNotebookTags = []
        self._PlotNotebookTagsIndex = 1        
        self._methodFilter = ''  
        self.methodType = MethodType()
        self.baseline = Baseline()
        self.legend_on = True
        self.units_on = True
        self._experimentList = []
        self.eisTypes = EISMeasurement()
        self.PSData = PSData
        self.files = []
        self._plots = {}
        self._titles = []
        self._titlesOn = False
        self._titleIndex = 0
        self.splitGraphs = False
        self._grouping = False
        self._groups = {}
    
    def show(self, experimentLabels = ''):
        # Experimental, use at own risk

        if self._PlotNotebookTagsIndex in self._PlotNotebookTags:
            self._PlotNotebookTagsIndex = 1 + self._PlotNotebookTagsIndex
        self._PlotNotebookTags.append(self._PlotNotebookTagsIndex)

        if self._titlesOn:        
            graphCount = self._getGraphCount()
            if len(self._titles) != graphCount:
                print('Title count incorrect. Set ' + str(len(self._titles)) + '/' + str(graphCount))
                return
        
        experimentIndex = 0
        canPlotAll = False
        for currentMethod in self.PSData.experimentList:    
            canplot = True

            if self._filterOnMethod and not self._methodFilter in currentMethod:
                # filtermethod set and check the method
                canplot = False
                    
            if not experimentLabels == '' and canplot:
                # check if this is the experiment we want to plot, if experimentLabels is set
                canplot =  self.PSData.experimentList[experimentIndex] in experimentLabels
        
            if canplot:
                canPlotAll = True
                if 'SWV' in currentMethod:
                    self._SWVAnalysis(self.PSData.data[self.PSData.experimentList[experimentIndex]],experimentIndex)
                if 'CV' in currentMethod:
                    self._CVAnalysis(self.PSData.data[self.PSData.experimentList[experimentIndex]],experimentIndex)
                    #print('CV')
                if 'EIS' in currentMethod:
                    self._EISAnalysis(self.PSData.data[self.PSData.experimentList[experimentIndex]],experimentIndex)
                    
            experimentIndex = experimentIndex + 1
            
        if canPlotAll:
            plt.show()
        else:
            if not self._methodFilter in experimentLabels:
                print('All plot() arguments are filtered out by the method filter')
            else:
                print('No data found for: ' + self.methodFilter)
                
    def _getGraphCount(self):
        ''' NB, change the amount of EIS graphs as they get developed '''
        eisCount =  len([i for i, s in enumerate(self.PSData.experimentList) if 'EIS' in s])*3
        swvCount = len([ i for i, s in enumerate(self.PSData.experimentList) if 'SWV' in s])
        cvCount = len([i for i, s in enumerate(self.PSData.experimentList) if 'CV' in s])

        # set to zero those we do not want to plot
        if not self.methodFilter in 'EIS':
            eisCount = 0
        if not self.methodFilter in 'SWV':
            swvCount = 0
        if not self.methodFilter in 'CV':
            cvCount = 0
        
        graphCount = 0
        if self.splitGraphs:
            # individual graphs, so count all
            graphCount = eisCount + swvCount + cvCount
        else:
            # all of each sort on a graph
            if eisCount > 0:
                graphCount += 3
            if swvCount > 0:
                graphCount += 1
            if cvCount > 0:
                graphCount += 1
        
        return graphCount
                
    def _SWVAnalysis(self, measurement, experimentIndex):
        # get units from the dictionary
        units = {}
        
        if (self.PSData.experimentList[experimentIndex] + ' Details') in self.PSData.data:
            units = self.PSData.data[self.PSData.experimentList[experimentIndex] + ' Details']
        else:
            units['x'] = {}
            units['y'] = {}
            units['x']['unit'] = ''
            units['y']['unit'] = ''
            units['x']['scale'] = 1
            units['y']['scale'] = 1
            units['title'] = ''

        PlotTag = str(self._PlotNotebookTagsIndex)
        
        if self.splitGraphs:
            # just create a new graph every time
            figx, axx = plt.subplots()
            axx.grid(True)
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            # check the dictionary for the graphs and add if exists
            
            tag = 'swv' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group

            if not tag in self._plots:
                figx, axx = plt.subplots()
                axx.grid(True)
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [figx, axx, titleIndex]
            else:
                plotdata = self._plots[tag]        
                figx = plotdata[0]
                axx = plotdata[1]
                titleIndex = plotdata[2]
        
        # generate the baseline
        self.baseline.generateBaseline(measurement.xvalues, measurement.yvalues)
        
        # subtract the baseline
        pos = 0
        ax_baseline = axis()
        for y in measurement.yvalues:
            ax_baseline.xvalues.append(measurement.xvalues[pos]/units['x']['scale'])
            ax_baseline.yvalues.append(self.baseline.subtract(measurement.xvalues[pos],y)/units['y']['scale'])
            pos = pos + 1
        
        # kind of backwards, translated to Ampere, and then we determine what would be the better scale
        XUnits = self._setScale(max(ax_baseline.xvalues))
        YUnits = self._setScale(max(ax_baseline.yvalues))
        
        yMod = []
        xMod = []
        
        for x in ax_baseline.xvalues:
            xMod.append(x/XUnits['scale'])
            
        for y in ax_baseline.yvalues:
            yMod.append(y/YUnits['scale'])

        axx.plot(xMod, yMod, label=(self.PSData.experimentList[experimentIndex] + ' : ' + units['title']))
        if self.units_on:
            axx.set_xlabel(XUnits['unit'] + 'V')
            axx.set_ylabel(YUnits['unit'] + 'A')
                
        if self.splitGraphs:
            if self._titlesOn:
                axx.set_title(self.titles[titleIndex])
            else:
                axx.set_title(self.PSData.experimentList[experimentIndex])
        else:
            axx.legend(bbox_to_anchor=(1.05,1.05))
            if self._titlesOn:
               axx.set_title(self.titles[titleIndex])
                   
                            
    def _CVAnalysis(self, measurement, experimentIndex):
        
        # get units from the dictionary
        units = {}
        if self.PSData.experimentList[experimentIndex] + ' Details' in self.PSData.data:
            units = self.PSData.data[self.PSData.experimentList[experimentIndex] + ' Details']
        else:
            units['x'] = {}
            units['y'] = {}
            units['x']['unit'] = ''
            units['y']['unit'] = ''
            units['x']['scale'] = 1
            units['y']['scale'] = 1

        PlotTag = str(self._PlotNotebookTagsIndex)
        
        if self.splitGraphs:
            # just create a new graph every time
            figx, axx = plt.subplots()
            titleIndex = self._titleIndex
            self._titleIndex += 1
            axx.grid(True)
        else:
            # check the dictionary for the graphs and add if exists
            
            tag = 'cv' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group
                            
            if not tag in self._plots:
                figx, axx = plt.subplots()
                axx.grid(True)
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [figx, axx, titleIndex]
            else:
                plotdata = self._plots[tag]        
                figx = plotdata[0]
                axx = plotdata[1]
                titleIndex = plotdata[2]
               
        # convert to ampere
        pos = 0
        ax = axis()
        for y in measurement.yvalues:
            ax.xvalues.append(measurement.xvalues[pos]/units['x']['scale'])
            ax.yvalues.append(y/units['y']['scale'])
            pos = pos + 1
        
        # and then go determine a better scale
        XUnits = self._setScale(max(ax.xvalues))
        YUnits = self._setScale(max(ax.yvalues))
        
        yMod = []
        xMod = []
        
        for x in ax.xvalues:
            xMod.append(x/XUnits['scale'])
            
        for y in ax.yvalues:
            yMod.append(y/YUnits['scale'])

        axx.plot(xMod,yMod, label=self.PSData.experimentList[experimentIndex]+ ' : ' + units['title'])
        
        if self.units_on:
            axx.set_xlabel(XUnits['unit'] + 'V')
            axx.set_ylabel(YUnits['unit'] + 'A')
        if self.splitGraphs:
            if self._titlesOn:
               axx.set_title(self.titles[titleIndex])
            else:
                axx.set_title(self.PSData.experimentList[experimentIndex])
        else:
            axx.legend(bbox_to_anchor=(1.05,1.05))
            if self._titlesOn:
                   axx.set_title(self.titles[titleIndex])

    def _EISAnalysis(self, measurement, experimentIndex):
        self._plotEISNyq(measurement, experimentIndex)
        self._plotEISZdashes(measurement, experimentIndex)
        self._plotEISYdash(measurement, experimentIndex)
        self._plotEISCap(measurement, experimentIndex)
        
    def _plotEISNyq(self, measurement, experimentIndex):

        PlotTag = str(self._PlotNotebookTagsIndex)

        if self.splitGraphs:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            tag = 'bode' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group + tag
            
            if not tag in self._plots:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [fig, ax1, ax2, titleIndex]
            else:
                plotdata = self._plots[tag]        
                fig = plotdata[0]
                ax1 = plotdata[1]
                ax2 = plotdata[2]
                titleIndex = plotdata[3]
                
        s = 4
        ax1.loglog(measurement.freq, measurement.Z,'s-', label=self.PSData.experimentList[experimentIndex], markersize=s)
        ax1.grid(True)
        ax2.plot(measurement.freq, measurement.phase,'*-', label=self.PSData.experimentList[experimentIndex], markersize=s)
        ax2.grid(True)
        b, t = ax1.get_ylim()
        b2, t2 = ax2.get_ylim()
        ax1.set_ylim([b/10, t*3])
        ax2.set_ylim([b2 - 10,t2 + 10])
        ax1.set_xlabel(self.eisTypes.freq)
        ax1.set_ylabel(self.eisTypes.Z + "/$\Omega$")
        ax2.set_ylabel(self.eisTypes.phase + "/$^\circ$")
        if self._titlesOn:
           ax1.set_title(self.titles[titleIndex])
           
        if self.splitGraphs:
            ax2.set_title(self.PSData.experimentList[experimentIndex])
        else:
            ax2.legend(bbox_to_anchor=(1.3,1.05))
            
    def _plotEISYdash(self, measurement, experimentIndex):

        PlotTag = ''
        if self.PlotNotebook:
            PlotTag = str(self._PlotNotebookTagsIndex) 

        if self.splitGraphs:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            
            tag = 'ydash' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group + tag
                            
            if not tag in self._plots:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [fig, ax1, ax2, titleIndex]
            else:
                plotdata = self._plots[tag]        
                fig = plotdata[0]
                ax1 = plotdata[1]
                ax2 = plotdata[2]
                titleIndex = plotdata[3]
        s = 4
        ax1.grid(True)
        
        XUnits = self._setScale(max(measurement.YRe))
        YUnits = self._setScale(max(measurement.YIm))
        
        yMod = []
        xMod = []
        
        for x in measurement.YRe:
            xMod.append(x/XUnits['scale'])
            
        for y in measurement.YIm:
            yMod.append(y/YUnits['scale'])
        
        
        ax1.plot(xMod, yMod,'*-', label=self.PSData.experimentList[experimentIndex], markersize=s)
        if self._titlesOn:
           ax1.set_title(self.titles[titleIndex])
        ax1.set_xlabel(self.eisTypes.YRe + "/" + XUnits['unit'] + "S")
        ax1.set_ylabel(self.eisTypes.YIm + "/" + YUnits['unit'] + "S")
           
        if self.splitGraphs:
            ax1.set_title(self.PSData.experimentList[experimentIndex])
        else:
            ax1.legend(bbox_to_anchor=(1.3,1.05))
           
    def _plotEISCap(self, measurement, experimentIndex):

        PlotTag = str(self._PlotNotebookTagsIndex)

        if self.splitGraphs:
            fig2, ax3 = plt.subplots()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            tag = 'cap' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group + tag
            
            if not tag in self._plots:
                fig2, ax3 = plt.subplots()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [fig2, ax3, titleIndex]
            else:
                plotdata = self._plots[tag]        
                fig2 = plotdata[0]
                ax3 = plotdata[1]
                titleIndex = plotdata[2]
        s = 4
        ax3.grid(True)
        
        XUnits = self._setScale(max(measurement.Cdash))
        YUnits = self._setScale(max(measurement.Cdashdash))
        
        cdMod = []
        cddMod = []
        for cdash in measurement.Cdash:
            cdMod.append(cdash/XUnits['scale'])
            
        for cdashdash in measurement.Cdashdash:
            cddMod.append(cdashdash/YUnits['scale'])
            
            
        ax3.plot(cddMod,cdMod,'o-', label=self.PSData.experimentList[experimentIndex], markersize=s)
        ax3.set_xlabel("C'/" + XUnits['unit'] + 'F')
        ax3.set_ylabel("C''/" + YUnits['unit'] + 'F')

        if self.splitGraphs:
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
               self._titleIndex += 1
            else:
                ax3.set_title(self.PSData.experimentList[experimentIndex])
        else:
            ax3.legend(bbox_to_anchor=(1.25,1.05))
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
               
    def _plotEISZdashes(self, measurement, experimentIndex):
        PlotTag = str(self._PlotNotebookTagsIndex)

        if self.splitGraphs:
            fig2, ax3 = plt.subplots()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            tag = 'Nyq' + PlotTag
            if self._grouping:
                for group in self._groups:
                    for item in self._groups[group]:
                        if self.PSData.experimentList[experimentIndex] in item:
                            tag = group + tag
            
            if not tag in self._plots:
                fig2, ax3 = plt.subplots()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots[tag] = [fig2, ax3, titleIndex]
            else:
                plotdata = self._plots[tag]        
                fig2 = plotdata[0]
                ax3 = plotdata[1]
                titleIndex = plotdata[2]
                
                
        XUnits = self._setScale(max(measurement.zdash))
        YUnits = self._setScale(max(measurement.zdashneg))
        
        xMod = []
        yMod = []
        for x in measurement.zdashneg:
            xMod.append(x/XUnits['scale'])
            
        for y in measurement.zdash:
            yMod.append(y/YUnits['scale'])
            
        s = 4
        ax3.grid(True)
        ax3.plot(xMod, yMod,'o-', label=self.PSData.experimentList[experimentIndex], markersize=s)
        ax3.set_xlabel(self.eisTypes.zdashneg + "/" + XUnits['unit'] + "$\Omega$")
        ax3.set_ylabel(self.eisTypes.zdash + "/" + YUnits['unit'] + "$\Omega$")

        if self.splitGraphs:
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
               self._titleIndex += 1
            else:
                ax3.set_title(self.PSData.experimentList[experimentIndex])
        else:
            ax3.legend(bbox_to_anchor=(1.05,1.05))
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
               
    def _setScale(self, value):
        value = abs(value)
        ret = {}
        ret['unit'] = ''
        ret['scale'] = 1
        
        if value < 0.009:
            ret['unit'] = 'm'
            ret['scale'] = 0.001
        if value < 0.000009:
            ret['unit'] = '\u03BC'
            ret['scale'] = 0.000001
        if value < 0.00000009:
            ret['unit'] = 'n'
            ret['scale'] = 0.00000001
        if value < 0.0000000009:
            ret['unit'] = 'p'
            ret['scale'] = 0.0000000001
        if value < 0.000000000009:
            ret['unit'] = 'f'
            ret['scale'] = 0.000000000001
        if value < 0.00000000000009:
            ret['unit'] = 'a'
            ret['scale'] = 0.00000000000001
            
        if value > pow(10,3):
            ret['unit'] = 'k'
            ret['scale'] = pow(10,3)
        if value > pow(10,6):
            ret['unit'] = 'M'
            ret['scale'] = pow(10,6)
        if value > pow(10,9):
            ret['unit'] = 'G'
            ret['scale'] = pow(10,9)
        if value > pow(10,12):
            ret['unit'] = 'T'
            ret['scale'] = pow(10,12)
            
        return ret
        
        
    def _getScale(self):
        if self.eisTypes.scale == pow(10,3):
            return 'k'
        if self.eisTypes.scale == pow(10,6):
            return 'M'
        if self.eisTypes.scale == pow(10,9):
            return 'G'
        if self.eisTypes.scale == pow(10,12):
            return 'T'
        return ''

    def _getUnits(self, curveTitle):
        details = curveTitle.split(" ")
        return [details[3], details[1]]
        
    
class MethodType:
    __slots__ = ['CV','SWV','EIS']
    
    def __init__(self):    
        self.CV = 'CV'
        self.SWV = 'SWV'
        self.EIS = 'EIS'
    
class Baseline:
    def __init__(self):
        self._startPosition = -1
        self._endPosition = -1
        self._subtractBaseline = False
        self._generatedBaseline = False
        self._gradient = 0
        self._constant = 0
        
    @property
    def startPosition(self):
        return self._startPosition
    
    @startPosition.setter
    def startPosition(self, val):
        self._subtractBaseline = True
        self._startPosition = val

    @property
    def endPosition(self):
        return self._endPosition
    
    @endPosition.setter
    def endPosition(self, val):
        self._endPosition = val
    
    def generateBaseline(self, x, y):
        if self._subtractBaseline:
            try:
                if self.endPosition == -1:
                    self.endPosition = len(y) - self.startPosition
                self._gradient = (y[self.startPosition] - y[self.endPosition])/(x[self.startPosition] - x[self.endPosition])
                self._constant = y[self.startPosition] - (x[self.startPosition]*self._gradient)
                self._generatedBaseline = True
            except:
                print('Exception: Could not generate baseline. Check validity of startPosition and endPosition.')
            
    def subtract(self, x, y):
        if self._subtractBaseline and self._generatedBaseline:
            return (y - (self._gradient*x + self._constant))
        return y

class EISMeasurement:
    __slots__ = ['freq','zdash','potential','zdashneg','Z','phase','current','npoints','tint','ymean','debugtext','Y','YRe','YIm','scale']
    
    def __init__(self):
        self.freq = "Frequency"
        self.zdash = "Z'"
        self.potential = "Potential"
        self.zdashneg = "-Z''"
        self.Z = "Z"
        self.phase = "-Phase"
        self.current = "Current"
        self.npoints = "npoints"
        self.tint = "tint"
        self.ymean = "ymean"
        self.debugtext = "debugtext"
        self.Y = "Y"
        self.YRe = "Y'"
        self.YIm = "Y''"
        self.scale = 100000 # standard set to mega ohms