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
        self.data = self.__parse(filename)
       
        
    def __parse(self, filename):
        try:
            f = open(filename, "rb")
            data = f.read().decode('utf-16').replace('\r\n',' ').replace(':true',r':"True"').replace(':false',r':"False"')
            f.close
        except:
            print('Could not find or open file: ' + filename)
            return
            
        try:
            data2 = data[0:(len(data) - 1)] # has a weird character at the end
            self.Data = json.loads(data2, object_hook=lambda d: SimpleNamespace(**d))
            self.__jsonParsed = True
        except:
            print('Failed to parse string to JSON')
            return
        
        try:
            for measurement in self.Data.measurements:
                currentMethod = self.__getMethodType(measurement.method).upper()
                index = len([i for i, s in enumerate(self._experimentList) if currentMethod in s])
                self._experimentList.append(currentMethod + ' ' + str(index + 1))
        except:
            print('Failed to generate property: experimentList')
            return
                
    def plot(self, experimentLabels = ''):
        # Experimental, use at own risk
        if not self.__jsonParsed:
            return
        
        units = []
        canPlotAll = False
        experimentIndex = 0    
        for measurement in self.Data.measurements:
            canplot = True
            currentMethod = self.__getMethodType(measurement.method).upper()
            
            if self.__filterOnMethod and not currentMethod in self._methodFilter:
                canplot = False
                
            if not experimentLabels == '' and canplot:
                canplot =  self._experimentList[experimentIndex] in experimentLabels
                
                
            if canplot:
                for curve in measurement.curves:
                    if currentMethod in self.methodType.SWV:
                        self.baseline.generateBaseline(curve.xaxisdataarray.datavalues, curve.yaxisdataarray.datavalues)
                    if self.units_on and len(units) <= 0:
                        units.append(self.__getUnits(curve.title))
                            
                    xvalues = []
                    yvalues = []
                    pos = 0
                    
                    for y in curve.yaxisdataarray.datavalues:
                        xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                        if currentMethod in self.methodType.SWV:
                            yvalues.append(self.baseline.subtract(curve.xaxisdataarray.datavalues[pos].v,y.v))
                        else:
                            yvalues.append(y.v)
                        pos = pos + 1
                    plt.plot(xvalues, yvalues, label=self._experimentList[experimentIndex])
                    canPlotAll = True
            experimentIndex = experimentIndex + 1
                    
        if canPlotAll:
            plt.grid(True)
            if self.legend_on:
                plt.legend(bbox_to_anchor=(1.05,1.05))
            if self.units_on and len(units) > 0:
                plt.xlabel(units[0][0])
                plt.ylabel(units[0][1])
            if self.title is not '':
                plt.title(self.title)
        else:
            if not self._methodFilter in experimentLabels:
                print('All plot() arguments are filtered out by the method filter')
            else:
                print('No data found for: ' + self.methodFilter)

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