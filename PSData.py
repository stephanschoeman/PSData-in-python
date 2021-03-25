# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:19:06 2021

@author: Stephan
"""
from types import SimpleNamespace
import simplejson as json

class Description:
    __slots__ = ['SWVParameters', 'CVParameters', 'Pretreatment', 'Technique']
    
    def __init__(self):
        self.SWVParameters = ''
        self.CVParameters = ''
        self.Pretreatment = ''
        self.Technique = ''

class Unit:
    __slots__ = ['type', 's', 'c', 't']
    
    def __init__(self):
        self.type = ''
        self.s = ''
        self.q = ''
        self.a = ''

class Datavalue:
    __slots__ = ['v', 's', 'c', 't']
    
    def __init__(self):
        self.v = 0.0
        self.s = 0
        self.c = 0
        self.t = ''
        
class Eisdatalist:
    __slots__ = ['appearance', 'title', 'hash', 'scantype', 'freqtype', 'cdc', 'fitvalues', 'dataset']
    
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
    __slots__ = ['type', 'arraytype', 'description', 'unit', 'datavalues', 'datavaluetype']
    
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''
    
class Dataset:
    __slots__ = ['type', 'values']
    
    def __init__(self):
        self.type = ''
        self.values = []
    
class Appearance:
    __slots__ = ['type', 'autoassigncolor', 'color', 'linewidth', 'symbolsize', 'symboltype', 'noline']
    
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
    __slots__ = ['type', 'arraytype', 'description', 'unit', 'datavalues', 'datavaluetype']
    
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''
     
class Yaxisdataarray:
    __slots__ = ['type', 'arraytype', 'description', 'unit', 'datavalues', 'datavaluetype']
    
    def __init__(self):
        self.type = ''
        self.arraytype = 0
        self.description = ''
        self.unit = Unit()
        self.datavalues = []
        self.datavaluetype = ''

class Peaklist:
    __slots__ = ['peaktype', 'left', 'right', 'peak', 'isign']
    
    def __init__(self):
        self.peaktype = 0
        self.left = 0
        self.right = 0
        self.peak = 0
        self.isign = 0

class Curve:
    __slots__ = ['appearance', 'title', 'hash', 'type', 'xaxis', 'xaxisdataarray', 'yaxisdataarray', 'meastype', 'peaklist', 'corrosionbutlervolmer', 'corrosiontafel']
    
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
    __slots__ = ['title','timestamp','utctimestamp','deviceused','deviceserial','devicefw','type','dataset','method','curves','eisdatalist']
    
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
    __slots__ = ['type','coreversion','methodformeasurement','measurements']
    
    def __init__(self):
        self.type = ''
        self.coreversion = ''
        self.methodformeasurement = ''
        self.measurements = []

class MethodType:
    __slots__ = ['CV','SWV','EIS']
    
    def __init__(self):    
        self.CV = 'CV'
        self.SWV = 'SWV'
        self.EIS = 'EIS'

class axis:
    __slots__ = ['xvalues','yvalues']
    
    def __init__(self):
        self.xvalues = []
        self.yvalues = []


class jparse:    
    @property
    def experimentList(self):
        return self._experimentList
    
    @property
    def parsedData(self):
        return self._parsedData
    
    @property
    def data(self):
        return self._data
    
    def __init__(self, filename):
        self._methodType = MethodType()
        self._experimentList = []
        self.files = []
        self._parsedData = self._parse(filename)
        self.experimentIndex = 0
        self._data = self._simplify()
       
        
    def _parse(self, filenames):
        self._getFilenames(filenames)
        
        try:
            index = 0
            readData = {}
            for filename in filenames:
                f = open(filename, "rb")
                readData[self.files[index]] = f.read().decode('utf-16').replace('\r\n',' ').replace(':true',r':"True"').replace(':false',r':"False"')
                index = index + 1
                f.close()
        except:
            print('Could not find or open file: ' + filename)
            return
            
        try:
            parsedData = {}
            for file in self.files:
                data2 = readData[file][0:(len(readData[file]) - 1)] # has a weird character at the end
                parsedData[file] = json.loads(data2, object_hook=lambda d: SimpleNamespace(**d))
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
    
    def _simplify(self):
        simplifiedData = {}
        experimentIndex = 0
        for file in self.files:
            rawData = self._parsedData[file]
            for measurement in rawData.measurements:
                currentMethod = self._getMethodType(measurement.method).upper()
                print(currentMethod)
                if currentMethod in self._methodType.SWV or currentMethod in self._methodType.CV:
                    simplifiedData[self._experimentList[experimentIndex]] = self._getXYDataPoints(measurement)
                experimentIndex = experimentIndex + 1
        
        return simplifiedData
        
    def _getXYDataPoints(self, measurement):
        ax = axis()
        for curve in measurement.curves:
            pos = 0
            for y in curve.yaxisdataarray.datavalues:
                ax.xvalues.append(curve.xaxisdataarray.datavalues[pos].v)
                ax.yvalues.append(y.v)
                pos = pos + 1
        return ax
            
    def _getFilenames(self, files):
        for f in files:
            file = f.split('\\')
            name = file[len(file) - 1].replace('.pssession','')
            self.files.append(name)
                
    def _getMethodType(self, method):
        methodName = ''
        splitted = method.split("\r\n")
        for line in splitted:
            if "METHOD_ID" in line:
                methodName = line.split("=")[1]
        return methodName
