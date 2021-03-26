# PSData in python
 Load a .pssession file into python for local processing.
 I do a bunch of [Cyclic Voltammetry](https://en.wikipedia.org/wiki/Cyclic_voltammetry) and [Square Wave Voltammetry](https://en.wikipedia.org/wiki/Squarewave_voltammetry) experiments regularly and wrote this Python script to extact my data for some post-processing. The main purpose is to skip additional export steps from the .pssession file, but I added plotting and baseline tools. I use [this](https://www.palmsens.com/product/palmsens4/) device for my measurements.
 
 **Supported experiments:**
 - Square wave voltammetry (primary)
 - Cyclic voltammetry
 - Electrical impedance spectroscopy
 
 **Files:**
 - PSData.py : this parses the .pssession data
 - SimplePSData.py : this is an example file to use the PSData object
 - PSDataPlot.py : this is the additional plotting functionality
 
 **Get started:**
 
 Download and install the dependencies if required.
 Place PSData.py and SimplePSData.py in the same directory.
 Open SimplePSData.py
 Replace the file directory in .jparse('') with the .pssession example provided.
 Run the code and you will be able to access the parsed data with:
 ```
 print(simpleData.experimentList) # list the experiments
 print(simpleData.data['SWV 1'].xvalues) # access the x values of the first experiment
 ```
 
 and that is about all you need to get started!
 
 **Dependencies:**
  - SimpleNamespace
  - simplejson
  - matplotlib (Only if you use PSDataPlot.py)

**PSData.py functionality:**

Assuming you use the following line of code to get your parsed data:

```simpleData = PS.jparse([r'C:\A.pssession',r'C:\B.pssession'])```

- List your experiments:
  ```simpleData.experimentList```
  These are listed as the program finds them.
- Find out where the experiment data comes from:
  ```simpleData.inFile('SWV 1')```
  The experiment tags come from the experimentList.
- SWV and CV x and y values can be accessed like this:
  ```simpleData.data['SWV 1'].xvalues``` and ```simpleData.data['SWV 1'].yvalues```
- EIS has the following parameters:
  - ```.freq```
  - ```.zdash```
  - ```.potential```
  - ```.zdashneg```
  - ```.Z```
  - ```.phase```
  - ```.npoints```
  - ```.tint```
  - ```.ymean```
  - ```.debugtext```
  - ```.Y```
  - ```.YRe``` (Ydash)
  - ```.YIm``` (Ydashdash)
  - These can be accessed in a similar way: ```simpleData.data['EIS 1'].potential```
  - They will not necessarily be available, depending on your experiment

**PSDataPlot.py functionality:**

If you want to use the plotting 'library', create the plot object from the simpleData:

```plot = PSP.PSPlot(simpleData)```

to do -> finish this section

**Example plots:**

Here is a raw SWV experiment plot:

![SWV Raw](https://user-images.githubusercontent.com/45431675/109668244-a7b75000-7b79-11eb-8dc4-b5c7c48f60fa.png)

and then I did a baseline subtraction on starting position 7:

![SWV Baseline](https://user-images.githubusercontent.com/45431675/109668187-95d5ad00-7b79-11eb-8362-1b34b6ae43ad.png)

Here is an example of two EIS measurements plotted together:

![EIS_Comp](https://user-images.githubusercontent.com/45431675/109689101-a3952d80-7b8d-11eb-9017-28dbb52d56c2.png)

Let me know if you have ideas for additional basic functionality.

ToDo:
- [ ] Curve smoothing with [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter)
- [ ] Peak detection
- [ ] Dynamic baseline by using the first and second derivatives
- [ ] Method summary printout and experiment grouping
- [ ] % peak comparison printout for grouped experiments
