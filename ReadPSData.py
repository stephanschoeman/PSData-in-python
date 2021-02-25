# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 19:23:21 2021

@author: Stephan

This is an example on how to use the PSData.py file
"""
from PSData import *

# just paste the file source here:
parsedData = PSSource(r'C:\Users\Stephan\Desktop\bik\hah\A.pssession')
parsedData.plot()

"""
parsedData.legend_on = True by default
parsedData.units_on = True by default
parsedData.title = "" by default

There is quite a bit of data within the PSData object that is usable
For example, the curve.title contains the units and method used in the experiment and the measurement.method has useful information

You can view the object structure in the PSData.py file for more information
or you can print the text (data2, line 110) and paste it in an online json converter for easy viewing

"""