# PSData in python
 Load a .pssession file into python for local processing
 
 Get started:
 Download and install the dependencies if required.
 Place PSData.py and ReadPsData.py in the same directory.
 Open ReadPsData.py
 Replace the file directory in PSSource('') with the .pssession example provided.
 Run the code and you should see a plot of the example data.
 
 **Dependencies:**
  - SimpleNamespace
  - simplejson
  - matplotlib

**How to use:**

Create the PSSource object that will contain all your data. The object creation automatically load the data into the object:
data = PS.PSSource(r'..\File.pssession')

You can then plot the data by using:
data.plot()

and that is about all you need to get started!

**Additional functionality (so far):**
- data.methodFilter = data.methodType.SWV will filter all plots on SWV. Also available: CV and EIS (not tested)
- data.baseline: (only available for SWV)
  - .startPosition set to int value of the position that you want to use for the baseline
  - .endPosition set to int value of the position that you want to use for the baseline
  - .subtractBaseline set to True to plot the subtracted values
