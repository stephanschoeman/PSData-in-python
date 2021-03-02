# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:19:06 2021

@author: Stephan
"""
from types import SimpleNamespace
import simplejson as json
import matplotlib.pyplot as plt

class Description:
    def __init__(self):
        self.SWVParameters = ''
        self.CVParameters = ''
        self.Pretreatment = ''
        self.Technique = ''

class Unit:
    def __init__(self):
        self.type = ''
        self.s = ''
        self.q = ''
        self.a = ''

class Datavalue:
    def __init__(self):
        self.v = 0.0
        self.s = 0
        self.c = 0
        self.t = ''
        
class Eisdatalist:
    def __init__(self):
        self.appearance = Appearance()
        self.title = ''
        self.hash = []
        self.scantype = 0
        self.freqype = 0
        self.cdc = object()
        self.fitvalues = object()
        self.dataset = Dataset()
    
class Value:
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''
    
class Dataset:
    def __init__(self):
        self.type = ''
        self.values = []
    
class Appearance:
    def __init__(self):
        self.type = ''
        self.autoassigncolor = False
        self.color = ''
        self.linewidth = 0
        self.symbolsize = 0
        self.symboltype = 0
        self.symbolfill = False
        self.noline = False
    
class Xaxisdataarray:
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''
     
class Yaxisdataarray:
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''

class Peaklist:
    def __init__(self):
        self.peaktpe = 0
        self.left = 0
        self.right = 0
        self.peak = 0
        self.isign = 0

class Curve:
    def __init__(self):
        self.appearance = Appearance()
        self.title = ''
        self.hash = []
        self.type = ''
        self.xaxis = 0
        self.yaxis = 0
        self.xaxisdataarray = Xaxisdataarray()
        self.yaxisdataarray = Yaxisdataarray()
        self.meastype = 0
        self.peaklist = []
        self.corrosionbutlervolmer = []
        self.corrosiontafel = []
    
class Measurement:
    def __init__(self):
        self.title = ''
        self.timestamp = object()
        self.utctimestamp = object()
        self.deviceused = 0
        self.deviceserial = ''
        self.devicefw = ''
        self.type = ''
        self.dataset = Dataset()
        self.method = ''
        self.curves = []
        self.eisdatalist = []
        
class Data:
    def __init__(self):
        self.type = ''
        self.coreversion = ''
        self.methodformeasurement = ''
        self.measurements = []
    
class MethodType:
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
                self._gradient = (y[self.startPosition].v - y[self.endPosition].v)/(x[self.startPosition].v - x[self.endPosition].v)
                self._constant = y[self.startPosition].v - (x[self.startPosition].v*self._gradient)
                self._generatedBaseline = True
            except:
                print('Exception: Could not generate baseline. Check validity of startPosition and endPosition.')
            
    def subtract(self, x, y):
        if self._subtractBaseline and self._generatedBaseline:
            return (y - (self._gradient*x + self._constant))
        return y

class EISMeasurement:
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
        self.YRe = "YRe"
        self.YIm = "YIm"
        self.scale = 100000 # standard set to mega ohms

class axis:
    def __init__(self):
        self.xvalues = []
        self.yvalues = []

class jparse:    
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
    def experimentList(self):
        return self._experimentList
    
    def __init__(self, filename):
        self._filterOnMethod = False
        self._methodFilter = ''  
        self.methodType = MethodType()
        self.baseline = Baseline()
        self.legend_on = True
        self.units_on = True
        self._jsonParsed = False
        self._experimentList = []
        self.eisTypes = EISMeasurement()
        self.datapoints = {}
        self.files = []
        self.data = self._parse(filename)
        self._plots = {}
        self._titles = []
        self._titlesOn = False
        self._titleIndex = 0
        self.splitGraphs = False
        
    def _parse(self, filenames):
        self._getFilenames(filenames)
        
        try:
            index = 0
            readData = {}
            for filename in filenames:
                f = open(filename, "rb")
                readData[self.files[index]] = f.read().decode('utf-16').replace('\r\n',' ').replace(':true',r':"True"').replace(':false',r':"False"')
                index = index + 1
                f.close
        except:
            print('Could not find or open file: ' + filename)
            return
            
        try:
            parsedData = {}
            for file in self.files:
                data2 = readData[file][0:(len(readData[file]) - 1)] # has a weird character at the end
                parsedData[file] = json.loads(data2, object_hook=lambda d: SimpleNamespace(**d))
            self._jsonParsed = True
        except:
            print('Failed to parse string to JSON')
            return
        
        try:
            for file in self.files:
                for measurement in parsedData[file].measurements:
                    currentMethod = self._getMethodType(measurement.method).upper()
                    index = len([i for i, s in enumerate(self._experimentList) if currentMethod in s])
                    self._experimentList.append(currentMethod + ' ' + str(index + 1))
        except:
            print('Failed to generate property: experimentList')
            return
        return parsedData
    
    def _getFilenames(self, files):
        for f in files:
            file = f.split('\\')
            name = file[len(file) - 1].replace('.pssession','')
            self.files.append(name)
                
    def plot(self, experimentLabels = ''):
        # Experimental, use at own risk
        if not self._jsonParsed:
            return

        if self._titlesOn:        
            graphCount = self._getGraphCount()
            if len(self._titles) != graphCount:
                print('Title count incorrect. Set ' + str(len(self._titles)) + '/' + str(graphCount))
                return
        
        experimentIndex = 0
        for file in self.files:
            data = self.data[file]
            canPlotAll = False
            for measurement in data.measurements:
                canplot = True
                currentMethod = self._getMethodType(measurement.method).upper()
                
                if self._filterOnMethod and not currentMethod in self._methodFilter:
                    canplot = False
                    
                if not experimentLabels == '' and canplot:
                    canplot =  self._experimentList[experimentIndex] in experimentLabels
                    
                if canplot:
                    if currentMethod in self.methodType.SWV:
                        self._SWVAnalysis(measurement,experimentIndex)
                    elif currentMethod in self.methodType.EIS:
                        self._EISAnalysis(measurement, experimentIndex)
                    else:
                        self._CVAnalysis(measurement, experimentIndex)
                    canPlotAll = True
                experimentIndex = experimentIndex + 1
                    
        if canPlotAll:
            plt.show()
        else:
            if not self._methodFilter in experimentLabels:
                print('All plot() arguments are filtered out by the method filter')
            else:
                print('No data found for: ' + self.methodFilter)
                
    def _getGraphCount(self):
        eisCount =  len([i for i, s in enumerate(self._experimentList) if self.methodType.EIS in s])*2
        swvCount = len([ i for i, s in enumerate(self._experimentList) if self.methodType.SWV in s])
        cvCount = len([i for i, s in enumerate(self._experimentList) if self.methodType.CV in s])
        overallCount = 0

        if not self.methodFilter in self.methodType.EIS:
            eisCount = 0
            overallCount += 2
        if not self.methodFilter in self.methodType.SWV:
            swvCount = 0
            overallCount += 1
        if not self.methodFilter in self.methodType.CV:
            cvCount = 0
            overallCount += 1
        
        graphCount = 0
        if self.splitGraphs:
            graphCount = eisCount + swvCount + cvCount
        else:
            if eisCount > 0:
                graphCount += 2
            if swvCount > 0:
                graphCount += 1
            if cvCount > 0:
                graphCount += 1
        
        return graphCount
                
    def _SWVAnalysis(self, measurement, experimentIndex):
        units = []
        titleIndex = 0
        if self.splitGraphs:
            figx, axx = plt.subplots()
            axx.grid(True)
            titleIndex = self._titleIndex
        else:
            if not 'swv' in self._plots:
                figx, axx = plt.subplots()
                axx.grid(True)
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots['swv'] = [figx, axx, titleIndex]
            else:
                plotdata = self._plots['swv']        
                figx = plotdata[0]
                axx = plotdata[1]
                titleIndex = plotdata[2]
        ax = axis()
        for curve in measurement.curves:
            self.baseline.generateBaseline(curve.xaxisdataarray.datavalues, curve.yaxisdataarray.datavalues)
            if self.units_on and len(units) <= 0:
                units.append(self._getUnits(curve.title))
            pos = 0
            for y in curve.yaxisdataarray.datavalues:
                ax.xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                ax.yvalues.append(self.baseline.subtract(curve.xaxisdataarray.datavalues[pos].v,y.v))
                pos = pos + 1
            self.datapoints[self._experimentList[experimentIndex]] = ax
            if self.units_on:
                axx.set_xlabel(units[0][0])
                axx.set_ylabel(units[0][1])
            axx.plot(ax.xvalues, ax.yvalues, label=self._experimentList[experimentIndex])
            if self.splitGraphs:
                if self._titlesOn:
                    axx.set_title(self.titles[titleIndex])
                else:
                    axx.set_title(self._experimentList[experimentIndex])
            else:
                axx.legend(bbox_to_anchor=(1.05,1.05))
                if self._titlesOn:
                   axx.set_title(self.titles[titleIndex])
                   
                            
    def _CVAnalysis(self, measurement, experimentIndex):
        units = []
        if self.splitGraphs:
            figx, axx = plt.subplots()
            titleIndex = self._titleIndex
            self._titleIndex += 1
            axx.grid(True)
        else:
            if not 'cv' in self._plots:
                figx, axx = plt.subplots()
                axx.grid(True)
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots['cv'] = [figx, axx, titleIndex]
            else:
                plotdata = self._plots['cv']        
                figx = plotdata[0]
                axx = plotdata[1]
                titleIndex = plotdata[2]
        ax = axis()
        for curve in measurement.curves:
            if self.units_on and len(units) <= 0:
                units.append(self._getUnits(curve.title))
            pos = 0
            for y in curve.yaxisdataarray.datavalues:
                ax.xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                ax.yvalues.append(y.v)
                pos = pos + 1
            self.datapoints[self._experimentList[experimentIndex]] = ax
        axx.plot(ax.xvalues, ax.yvalues, label=self._experimentList[experimentIndex])
        if self.units_on:
            axx.set_xlabel(units[0][0])
            axx.set_ylabel(units[0][1])
        if self.splitGraphs:
            if self._titlesOn:
               axx.set_title(self.titles[titleIndex])
               self._titleIndex += 1
            else:
                axx.set_title(self._experimentList[experimentIndex])
        else:
            axx.legend(bbox_to_anchor=(1.05,1.05))
            if self._titlesOn:
                   axx.set_title(self.titles[titleIndex])

    def _EISAnalysis(self, measurement, experimentIndex):
        eisdata = {}                    
        for eis in measurement.eisdatalist:
            for value in eis.dataset.values:
                v = []
                for c in value.datavalues:
                    val = c.v
                    if value.unit.q == self.eisTypes.zdash or value.unit.q == self.eisTypes.zdashneg:
                        val = c.v/self.eisTypes.scale
                    v.append(val)
                eisdata[value.unit.q] = v                                    
        
        if self.splitGraphs:
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            if not 'bode' in self._plots:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots['bode'] = [fig, ax1, ax2, titleIndex]
            else:
                plotdata = self._plots['bode']        
                fig = plotdata[0]
                ax1 = plotdata[1]
                ax2 = plotdata[2]
                titleIndex = plotdata[3]

        ax1.loglog(eisdata[self.eisTypes.freq], eisdata[self.eisTypes.Z], 's-', label=self._experimentList[experimentIndex])
        ax1.grid(True)
        ax2.plot(eisdata[self.eisTypes.freq], eisdata[self.eisTypes.phase], '*-', label=self._experimentList[experimentIndex])
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
            ax2.set_title(self._experimentList[experimentIndex])
        else:
            ax2.legend(bbox_to_anchor=(1.3,1.05))
        
        if self.splitGraphs:
            fig2, ax3 = plt.subplots()
            titleIndex = self._titleIndex
            self._titleIndex += 1
        else:
            if not 'Nyq' in self._plots:
                fig2, ax3 = plt.subplots()
                titleIndex = self._titleIndex
                self._titleIndex += 1
                self._plots['Nyq'] = [fig2, ax3, titleIndex]
            else:
                plotdata = self._plots['Nyq']        
                fig2 = plotdata[0]
                ax3 = plotdata[1]
                titleIndex = plotdata[2]
        
        ax3.grid(True)
        ax3.plot(eisdata[self.eisTypes.zdash], eisdata[self.eisTypes.zdashneg], 'o-', label=self._experimentList[experimentIndex])
        ax3.set_xlabel(self.eisTypes.zdashneg + "/" + self._getScale() + "$\Omega$")
        ax3.set_ylabel(self.eisTypes.zdash + "/" + self._getScale() + "$\Omega$")
        self.datapoints[self.experimentList[experimentIndex]] = eisdata
        if self.splitGraphs:
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
               self._titleIndex += 1
            else:
                ax3.set_title(self._experimentList[experimentIndex])
        else:
            ax3.legend(bbox_to_anchor=(1.05,1.05))
            if self._titlesOn:
               ax3.set_title(self.titles[titleIndex])
            
        
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
        
    def _getMethodType(self, method):
        methodName = ''
        splitted = method.split("\r\n")
        for line in splitted:
            if "METHOD_ID" in line:
                methodName = line.split("=")[1]
        return methodName