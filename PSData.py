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
        self.All = ''
    
class Baseline:
    def __init__(self):
        self._startPosition = -1
        self._endPosition = -1
        self.__subtractBaseline = False
        self.__generatedBaseline = False
        self.__gradient = 0
        self.__constant = 0
        
    @property
    def startPosition(self):
        return self._startPosition
    
    @startPosition.setter
    def startPosition(self, val):
        self.__subtractBaseline = True
        self._startPosition = val

    @property
    def endPosition(self):
        return self._endPosition
    
    @endPosition.setter
    def endPosition(self, val):
        self._endPosition = val
    
    def generateBaseline(self, x, y):
        if self.__subtractBaseline:
            try:
                if self.endPosition == -1:
                    self.endPosition = len(y) - self.startPosition
                self.__gradient = (y[self.startPosition].v - y[self.endPosition].v)/(x[self.startPosition].v - x[self.endPosition].v)
                self.__constant = y[self.startPosition].v - (x[self.startPosition].v*self.__gradient)
                self.__generatedBaseline = True
            except:
                print('Exception: Could not generate baseline. Check validity of startPosition and endPosition.')
            
    def subtract(self, x, y):
        if self.__subtractBaseline and self.__generatedBaseline:
            return (y - (self.__gradient*x + self.__constant))
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
    def methodFilter(self):
        return self._methodFilter
    
    @methodFilter.setter
    def methodFilter(self, val):
        self.__filterOnMethod = True
        self._methodFilter = val
    
    @property
    def experimentList(self):
        return self._experimentList
    
    def __init__(self, filename):
        self.__filterOnMethod = False
        self._methodFilter = ''  
        self.methodType = MethodType()
        self.baseline = Baseline()
        self.legend_on = True
        self.units_on = True
        self.title = ''
        self.__jsonParsed = False
        self._experimentList = []
        self.eisTypes = EISMeasurement()
        self.datapoints = {}
        self.files = []
        self.data = self.__parse(filename)
        self.__plots = {}
        self.splitGraphs = False
       
        
    def __parse(self, filenames):
        self.__getFilenames(filenames)
        
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
            self.__jsonParsed = True
        except:
            print('Failed to parse string to JSON')
            return
        
        try:
            for file in self.files:
                for measurement in parsedData[file].measurements:
                    currentMethod = self.__getMethodType(measurement.method).upper()
                    index = len([i for i, s in enumerate(self._experimentList) if currentMethod in s])
                    self._experimentList.append(currentMethod + ' ' + str(index + 1))
        except:
            print('Failed to generate property: experimentList')
            return
        return parsedData
    
    def __getFilenames(self, files):
        for f in files:
            file = f.split('\\')
            name = file[len(file) - 1].replace('.pssession','')
            self.files.append(name)
                
    def plot(self, experimentLabels = ''):
        # Experimental, use at own risk
        if not self.__jsonParsed:
            return
        
        experimentIndex = 0
        for file in self.files:
            data = self.data[file]
            units = []
            canPlotAll = False
            
            
            for measurement in data.measurements:
                canplot = True
                currentMethod = self.__getMethodType(measurement.method).upper()
                
                if self.__filterOnMethod and not currentMethod in self._methodFilter:
                    canplot = False
                    
                if not experimentLabels == '' and canplot:
                    canplot =  self._experimentList[experimentIndex] in experimentLabels
                    
                if canplot:
                    xvalues = []
                    yvalues = []
                    if not currentMethod in self.methodType.EIS:
                        if self.splitGraphs:
                            figx, axx = plt.subplots()
                            axx.grid(True)
                        ax = axis()
                        for curve in measurement.curves:
                            if currentMethod in self.methodType.SWV:
                                self.baseline.generateBaseline(curve.xaxisdataarray.datavalues, curve.yaxisdataarray.datavalues)
                            if self.units_on and len(units) <= 0:
                                units.append(self.__getUnits(curve.title))
                                if not self.splitGraphs:
                                    figx, axx = plt.subplots()
                            pos = 0
                            for y in curve.yaxisdataarray.datavalues:
                                xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                                if currentMethod in self.methodType.SWV:
                                    yvalues.append(self.baseline.subtract(curve.xaxisdataarray.datavalues[pos].v,y.v))
                                else:
                                    yvalues.append(y.v)
                                pos = pos + 1
                            ax.xvalues = xvalues
                            ax.yvalues = yvalues
                            self.datapoints[self._experimentList[experimentIndex]] = ax
                            if self.units_on:
                                axx.set_xlabel(units[0][0])
                                axx.set_ylabel(units[0][1])
                            axx.plot(xvalues, yvalues, label=self._experimentList[experimentIndex])
                            axx.set_title(self._experimentList[experimentIndex])
                            canPlotAll = True
                    else:
                       self.__EISAnalysis(measurement, experimentIndex)
                       canPlotAll = True
                experimentIndex = experimentIndex + 1
                    
        if canPlotAll:
            plt.grid(True)
            if self.legend_on and not self.splitGraphs:
                plt.legend(bbox_to_anchor=(1.05,1.05))
            if self.title is not '':
                plt.title(self.title)
            plt.show()
        else:
            if not self._methodFilter in experimentLabels:
                print('All plot() arguments are filtered out by the method filter')
            else:
                print('No data found for: ' + self.methodFilter)
                
    def __EISAnalysis(self, measurement, experimentIndex):
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
        else:
            if not 'bode' in self.__plots:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                self.__plots['bode'] = [fig, ax1, ax2]
            else:
                plotdata = self.__plots['bode']        
                fig = plotdata[0]
                ax1 = plotdata[1]
                ax2 = plotdata[2]

        ax1.loglog(eisdata[self.eisTypes.freq], eisdata[self.eisTypes.Z], 's-')
        ax1.grid(True)
        ax2.plot(eisdata[self.eisTypes.freq], eisdata[self.eisTypes.phase], '*-')
        ax2.grid(True)
        b, t = ax1.get_ylim()
        b2, t2 = ax2.get_ylim()
        ax1.set_ylim([b/10, t*3])
        ax2.set_ylim([b2 - 10,t2 + 10])
        ax1.set_xlabel(self.eisTypes.freq)
        ax1.set_ylabel(self.eisTypes.Z + "/$\Omega$")
        ax2.set_ylabel(self.eisTypes.phase + "/$^\circ$")
        
        if self.splitGraphs:
            fig2, ax3 = plt.subplots()
        else:
            if not 'Nyq' in self.__plots:
                fig2, ax3 = plt.subplots()
                self.__plots['Nyq'] = [fig2, ax3]
            else:
                plotdata = self.__plots['Nyq']        
                fig2 = plotdata[0]
                ax3 = plotdata[1]
        
        ax3.grid(True)
        ax3.plot(eisdata[self.eisTypes.zdash], eisdata[self.eisTypes.zdashneg], 'o-')
        ax3.set_xlabel(self.eisTypes.zdashneg + "/" + self.__getScale() + "$\Omega$")
        ax3.set_ylabel(self.eisTypes.zdash + "/" + self.__getScale() + "$\Omega$")
        self.datapoints[self.experimentList[experimentIndex]] = eisdata
        
    def __getScale(self):
        if self.eisTypes.scale == pow(10,3):
            return 'k'
        if self.eisTypes.scale == pow(10,6):
            return 'M'
        if self.eisTypes.scale == pow(10,9):
            return 'G'
        if self.eisTypes.scale == pow(10,12):
            return 'T'
        return ''

    def __getUnits(self, curveTitle):
        details = curveTitle.split(" ")
        return [details[3], details[1]]
        
    def __getMethodType(self, method):
        methodName = ''
        splitted = method.split("\r\n")
        for line in splitted:
            if "METHOD_ID" in line:
                methodName = line.split("=")[1]
        return methodName