# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:19:06 2021

@author: Stephan
"""
from types import SimpleNamespace
import simplejson as json
import matplotlib.pyplot as plt

class Description:
    SWVParameters = ''
    CVParameters = ''
    Pretreatment = ''
    Technique = ''

class Unit:
    type = ''
    s = ''
    q = ''
    a = ''

class Datavalue:
    v = 0.0
    s = 0
    c = 0
    
class Value:
    type = ''
    arraytype = 0
    description = ''
    unit = Unit()
    datavalues = []
    datavaluetype = ''
    
class Dataset:
    type = ''
    values = []
    
class Appearance:
    type = ''
    autoassigncolor = False
    color = ''
    linewidth = 0
    symbolsize = 0
    symboltype = 0
    symbolfill = False
    noline = False
    
class Xaxisdataarray:
    type = ''
    arraytype = 0
    description = ''
    unit = Unit()
    datavalues = []
    datavaluetype = ''
     
class Yaxisdataarray:
    type = ''
    arraytype = 0
    description = ''
    unit = Unit()
    datavalues = []
    datavaluetype = ''

class Peaklist:
    peaktpe = 0
    left = 0
    right = 0
    peak = 0
    isign = 0

class Curve:
    appearance = Appearance()
    title = ''
    hash = []
    type = ''
    xaxis = 0
    yaxis = 0
    xaxisdataarray = Xaxisdataarray()
    yaxisdataarray = Yaxisdataarray()
    meastype = 0
    peaklist = []
    corrosionbutlervolmer = []
    corrosiontafel = []
    
class Measurement:
        title = ''
        timestamp = object()
        utctimestamp = object()
        deviceused = 0
        deviceserial = ''
        devicefw = ''
        type = ''
        dataset = Dataset()
        method = ''
        curves = []
        eisdatalist = []
        
class Data:
    type = ''
    coreversion = ''
    methodformeasurement = ''
    measurements = []
    
class MethodType:
    CV = 'CV'
    SWV = 'SWV'
    EIS = 'EIS'
    All = ''
    
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
        if self.__subtractBaseline:
            return (y - (self.__gradient*x + self.__constant))
        return y

class PSSource:
    @property
    def methodFilter(self):
        return self._methodFilter
    
    @methodFilter.setter
    def methodFilter(self, val):
        self.__filterOnMethod = True
        self._methodFilter = val
    
    def __init__(self, filename):
        self.__filterOnMethod = False
        self._methodFilter = ''  
        self.methodType = MethodType()
        self.baseline = Baseline()
        self.legend_on = True
        self.units_on = True
        self.title = ''
        self.__jsonParsed = False
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
        
    def plot(self):
        # Experimental, use at own risk
        if not self.__jsonParsed:
            return
        
        shortlistOfMethods = {}
        units = []
        CanPlotAll = False
            
        for measurement in self.Data.measurements:
            canplot = True
            currentMethod = self.__getMethodType(measurement.method).upper()
            
            if self.__filterOnMethod and not currentMethod in self._methodFilter:
                canplot = False
            
            if canplot:
                if currentMethod in shortlistOfMethods:
                    shortlistOfMethods[currentMethod] = shortlistOfMethods[currentMethod] + 1
                    i = shortlistOfMethods[currentMethod]
                else:
                    i = 1
                    shortlistOfMethods[currentMethod] = i
                currentLabel = currentMethod + ' ' + str(i)
                
                for curve in measurement.curves:
                    if self.methodFilter is self.methodType.SWV:
                        self.baseline.generateBaseline(curve.xaxisdataarray.datavalues, curve.yaxisdataarray.datavalues)
                    elif len(units) <= 0: #hopefully only 1 print, but not important
                        print("Cannot do baseline subtraction for any other method but SWV, yet!")
                    
                    if self.units_on and len(units) <= 0:
                        units.append(self.__getUnits(curve.title))
                            
                    xvalues = []
                    yvalues = []
                    pos = 0
                    
                    for y in curve.yaxisdataarray.datavalues:
                        xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                        yvalues.append(self.baseline.subtract(curve.xaxisdataarray.datavalues[pos].v,y.v))
                        pos = pos + 1
                    plt.plot(xvalues, yvalues, label=currentLabel)
                    CanPlotAll = True
                    
        if CanPlotAll:
            plt.grid(True)
            if self.legend_on:
                plt.legend(bbox_to_anchor=(1.05,1.05))
            if self.units_on and len(units) > 0:
                plt.xlabel(units[0][0])
                plt.ylabel(units[0][1])
            if self.title is not '':
                plt.title(self.title)
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