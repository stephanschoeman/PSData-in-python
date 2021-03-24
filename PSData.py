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
                
