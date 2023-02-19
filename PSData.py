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

class EISMeasurement:
    __slots__ = ['freq','zdash','potential','zdashneg','Z','phase','current','npoints','tint','ymean','debugtext','Y','YRe','YIm','scale','Cdash','Cdashdash']
    
    def __init__(self):
        self.freq = []
        self.zdash = []
        self.potential = []
        self.zdashneg = []
        self.Z = []
        self.phase = []
        self.current = []
        self.npoints = []
        self.tint = []
        self.ymean = []
        self.debugtext = []
        self.Y = []
        self.YRe = []
        self.YIm = []
        self.Cdash = []
        self.Cdashdash = []
        self.scale = 100000 # standard set to mega ohms

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
        self.experimentToFileMap = {}
        self._data = self._simplify()
        
    def _parse(self, filenames):
        # takes in the files
        # parses the raw data to an object
        # simplifies the values and adds it to the 'data' object
        
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
                for measurement in parsedData[file].Measurements:
                    currentMethod = self._getMethodType(measurement.Method).upper()
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
            for measurement in rawData.Measurements:
                currentMethod = self._getMethodType(measurement.Method).upper()
                if currentMethod in self._methodType.SWV or currentMethod in self._methodType.CV:
                    simplifiedData[self._experimentList[experimentIndex]] = self._getXYDataPoints(measurement)
                    simplifiedData[self._experimentList[experimentIndex] + ' Details'] = self._getXYUnits(measurement)
                if currentMethod in self._methodType.EIS:
                    simplifiedData[self._experimentList[experimentIndex]] = self._getEISDataPoints(measurement)
                self.experimentToFileMap[self._experimentList[experimentIndex]] = file
                experimentIndex = experimentIndex + 1

        
        return simplifiedData
    
    def _getXYUnits(self, measurement):
        unit = {}
        try:
            xtext = measurement.Curves[0].XAxisDataArray.Unit.Type
            ytext = measurement.Curves[0].YAxisDataArray.Unit.Type
            if xtext is not None:
                unit['x'] = self._unitTextToScale(xtext)
                unit['y'] = self._unitTextToScale(ytext)
            unit['title'] = measurement.Title
        except:
            print('Exception when processing units for SWV or CV.')
            unit = {}
        return unit
        
    
    def _unitTextToScale(self, text):
        unit = {}
        unit['scale'] = 1
        unit['unit'] = ''
        
        if 'Milli' in text:
            unit['scale'] = 1000
            unit['unit'] = 'm'
        if 'Micro' in text:
            unit['scale'] = 1000000
            unit['unit'] = "\u03BC"
        if 'Nano' in text:
            unit['scale'] = 1000000000
            unit['unit'] = 'n'
        if 'Pico' in text:
            unit['scale'] = 1000000000000
            unit['unit'] = 'p'
            
        return unit
    
    def _getXYDataPoints(self, measurement):
        ax = axis()
        for curve in measurement.Curves:
            pos = 0
            for y in curve.YAxisDataArray.DataValues:
                ax.xvalues.append(curve.XAxisDataArray.DataValues[pos].V)
                ax.yvalues.append(y.V)
                pos = pos + 1
        return ax
    
    def _getEISDataPoints(self, measurement):
        eisdata = EISMeasurement()                   
        for eis in measurement.EISDataList:
            for value in eis.DataSet.Values:
                if value.Unit.Q is not None:
                    v = []
                    for c in value.DataValues:
                        v.append(c.V)
                    if value.Unit.Q == "Frequency":
                        eisdata.freq = v
                    if value.Unit.Q == "Z'":
                        eisdata.zdash = v
                    if value.Unit.Q == "Potential'":
                        eisdata.potential = v
                    if value.Unit.Q == "-Z''":
                        eisdata.zdashneg = v
                    if value.Unit.Q == "Z":
                        eisdata.Z = v
                    if value.Unit.Q == "-Phase":
                        eisdata.phase = v
                    if value.Unit.Q == "npoints":
                        eisdata.npoints = v
                    if value.Unit.Q == "tint":
                        eisdata.tint = v
                    if value.Unit.Q == "ymean":
                        eisdata.ymean = v
                    if value.Unit.Q == "debugtext":
                        eisdata.debugtext = v
                    if value.Unit.Q == "Y":
                        eisdata.Y = v
                    if value.Unit.Q == "Y'":
                        eisdata.YRe = v
                    if value.Unit.Q == "Y''":
                        eisdata.YIm = v
                        
        pos = 0
        cd = []
        cdd = []
        for zdd in eisdata.zdashneg:
            denom = 2*3.141592653589793*eisdata.freq[pos]*(eisdata.zdash[pos]*eisdata.zdash[pos] + eisdata.zdashneg[pos]*eisdata.zdashneg[pos])
            cdd.append(zdd/(denom))
            cd.append(eisdata.zdash[pos]/(denom))
            pos += 1
        
        eisdata.Cdash = cd
        eisdata.Cdashdash = cdd
        
        return eisdata
            
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
    
    def inFile(self, experimentLabel):
        if experimentLabel in self.experimentToFileMap:
            print(experimentLabel + ' is in ' +  self.experimentToFileMap[experimentLabel] + ".pssession")
