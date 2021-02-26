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
    startPosition = -1
    endPosition = -1
    subtractBaseline = False
    __generatedBaseline = False
    __gradient = 0
    __constant = 0
    
    def generateBaseline(self, x, y):
        try:
            if self.startPosition > -1:
                if self.endPosition == -1:
                    self.endPosition = len(y) - self.startPosition
                self.__gradient = (y[self.startPosition].v - y[self.endPosition].v)/(x[self.startPosition].v - x[self.endPosition].v)
                self.__constant = y[self.startPosition].v - (x[self.startPosition].v*self.__gradient)
                self.__generatedBaseline = True
            else:
                print('Could not generate baseline. Set startPosition and endPosition')
        except:
            print('Exception: Could not generate baseline. Check validity of startPosition and endPosition.')
            
    def subtract(self, x, y):
        if self.subtractBaseline:
            return (y - (self.__gradient*x + self.__constant))
        return y

class PSSource:
    methodType = MethodType()
    baseline = Baseline()
    legend_on = True
    units_on = True
    title = ''
    methodFilter = ''
    __jsonParsed = False
    
    def __init__(self, filename):
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
        
        got_units = False
        method = []
        shortlistOfMethods = {}
        units = []
        filterMethods = False
        gCanPlot = False
        if not self.methodFilter == '':
            filterMethods = True
            
        for measurement in self.Data.measurements:
            canplot = True
            currentMethod = self.__getMethodType(measurement.method).upper()
            
            if filterMethods:
                if not currentMethod in self.methodFilter:
                    canplot = False
            
            if canplot:
                if currentMethod in shortlistOfMethods:
                    shortlistOfMethods[currentMethod] = shortlistOfMethods[currentMethod] + 1
                    i = shortlistOfMethods[currentMethod]
                else:
                    i = 1
                    shortlistOfMethods[currentMethod] = i
                lab = currentMethod + ' ' + str(i)
                method.append(lab)
                for curve in measurement.curves:
                    if self.units_on:
                        if not got_units:
                            units.append(self.__getUnits(curve.title))
                            got_units = True
                            
                    xvalues = []
                    yvalues = []
                    pos = 0
                    
                    if self.baseline.subtractBaseline:
                        if self.methodFilter is self.methodType.SWV:
                            self.baseline.generateBaseline(curve.xaxisdataarray.datavalues, curve.yaxisdataarray.datavalues)
                        else:
                            self.baseline.subtractBaseline = False
                            print("Cannot do baseline subtraction for any other method but SWV, yet!")
                    else:
                        self.baseline.subtractBaseline = False
                    
                    for y in curve.yaxisdataarray.datavalues:
                        xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                        yvalues.append(self.baseline.subtract(curve.xaxisdataarray.datavalues[pos].v,y.v))
                        pos = pos + 1
                    plt.plot(xvalues, yvalues, label=lab)
                    plt.grid(True)
                    gCanPlot = True
        if gCanPlot:
            if self.legend_on:
                plt.legend(bbox_to_anchor=(1.05,1.05))
            if self.units_on and got_units:
                plt.xlabel(units[0][0])
                plt.ylabel(units[0][1])
            if self.title is not '':
                plt.title(self.title)
        else:
            print('No data found for: ' + self.methodFilter)

    def __getUnits(self, curveTitle):
        details = curveTitle.split(" ")
        return [details[3], details[1]]
        
    def __getMethodType(self,method):
        methodName = ''
        splitted = method.split("\r\n")
        for line in splitted:
            if "METHOD_ID" in line:
                methodName = line.split("=")[1]
        return methodName