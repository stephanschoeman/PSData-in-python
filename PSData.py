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

class PSSource:
    methodType = MethodType()
    legend_on = True
    units_on = True
    __jsonParsed = False
    title = ''
    methodFilter = ''
    
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
                    for x in curve.xaxisdataarray.datavalues:
                        xvalues.append(x.v)
                    for y in curve.yaxisdataarray.datavalues:
                        yvalues.append(y.v)
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