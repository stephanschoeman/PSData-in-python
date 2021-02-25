# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:19:06 2021

@author: Stephan
"""
from types import SimpleNamespace
import simplejson as json

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
    
class PSSource:
    def __init__(self, filename):
        f = open(filename, "rb")
        data = f.read().decode('utf-16').replace('\r\n',' ').replace(':true',r':"True"').replace(':false',r':"False"')
        f.close
        data2 = data[0:(len(data) - 1)]
        self.Data = json.loads(data2, object_hook=lambda d: SimpleNamespace(**d))