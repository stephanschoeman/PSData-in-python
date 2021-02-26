# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 19:23:21 2021

@author: Stephan

This is an example on how to use the PSData.py file
"""
import PSData as PS

# just paste the file source here:
data = PS.PSSource(r'C:\Users\Stephan\Documents\PhD\Testing\20210220\J.pssession')
data.methodFilter = data.methodType.SWV
#data.baseline.startPosition = 5
data.plot()

"""
legend_on = True by default
units_on = True by default
title = "" by default
methodFilter = all by default. Options are SWV, CV, and EIS. All string values.

baseline creates a linear baseline using a start and end position on each curve
data.baseline.startPosition = set to int value
data.baseline.endPosition = set to end - startPosition if left empty
data.baseline.subtractBaseline = must be True to subtract baseline

There is quite a bit of data within the PSData object that is usable
For example, the curve.title contains the units and method used in the experiment and the measurement.method has useful information

You can view the object structure in the PSData.py file for more information
or you can print the text (data2, line 118) and paste it in an online json converter for easy viewing

"""