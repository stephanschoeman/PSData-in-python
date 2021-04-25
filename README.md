# PSData in python
 Load a .pssession file into python for local processing.
 I do a bunch of [Cyclic Voltammetry](https://en.wikipedia.org/wiki/Cyclic_voltammetry) and [Square Wave Voltammetry](https://en.wikipedia.org/wiki/Squarewave_voltammetry) experiments regularly and wrote this Python script to extact my data for some post-processing. The main purpose is to skip additional export steps from the .pssession file, but I added plotting and baseline tools. I use [this](https://www.palmsens.com/product/palmsens4/) device for my measurements.
 
## Supported experiments:
 - Square wave voltammetry (primary)
 - Cyclic voltammetry
 - Electrical impedance spectroscopy
 
## Files:
 - PSData.py : this parses the .pssession data
 - SimplePSData.py : this is an example file to use the PSData object
 - PSDataPlot.py : this is the additional plotting functionality
 
## Dependencies:
  - SimpleNamespace
  - simplejson
  - matplotlib (Only if you use PSDataPlot.py)
 
## Get started: 
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

## PSData.py functionality:

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
  
  These can be accessed in a similar way: ```simpleData.data['EIS 1'].potential```
  
  They will not necessarily be available, depending on your experiment

## PSDataPlot.py functionality:

If you want to use the plotting 'library', create the plot object from the simpleData:

```plot = PSP.PSPlot(simpleData)```

And then you can plot the data using:

```plot.show()```

The graphs are joined by type, but if you want to split the experiments, set the following:

```plot.splitGraphs = True```

You can set the titles of the graphs by populating the ```plot.titles``` list. If there are three graphs, you obviously need three titles:

```plot.titles = ['Title 1', 'Title 2', 'Title 3']```

You can filter on method to plot only a specific method:

```plot.methodFilter = 'EIS'```

You can set a baseline for SWV graphs by setting the beginning and end points for the baseline. It creates a linear baseline between the two points and subtracts it from the measured values:

```plot.baseline.startPosition = 5```

```plot.baseline.endPosition = 65```

If you want to reset the baseline (if you repeadedly use the ```.show()``` command), then you can between the graphs use the reset statement:

```
plot.baseline.startPosition = 5
plot.show(['SWV 1'])
plot.baseline.resetBaseline = True
plot.show(['SWV 1'])
```

Something experimental, you can group the experiments using the grouping tag and adding a dictionary of the groups to it:

```plot.groups = {'G1':{'SWV 1','SWV 2'},'G2':{'SWV 3', 'SWV 4'},'G3':{'CV 1'},'G4':{'CV 2'}}```

the group tags are not used except for lookups.

Lastly, if you want to plot specific experiments instead, fill in the experiment labels of the required experiments:

```plot.show(['SWV 1', 'CV 3'])```

## Addtional notes:
I use Jupyter Notebooks for my work. If you use this, the variables are stored per plot object. This means if you set a variable (like the baseline) in a cell and you run the cell above it again with the same plot object the baseline variable will be used in that cell as well.

You can overcome this by creating a new plot object per cell (which is tedious) or you can execute the cells in sequential order if you need to run cells above the current working cell. You are able to use the ```.show()``` command in different cells, so if you analyse your data in this way just make sure that you either reset the variables you have used before, or run everything sequentially.

I will have a look around to overcome this some time in the future :)

## Example plots:

SWV and Cyclic voltammetry:

![swv](https://user-images.githubusercontent.com/45431675/112733973-a6483000-8f4b-11eb-96b1-cfd73bab65f0.png)
![cv](https://user-images.githubusercontent.com/45431675/112733990-ba8c2d00-8f4b-11eb-9045-fff9c78b7b7f.png)

Here is an example of an EIS experiment:

![eis2](https://user-images.githubusercontent.com/45431675/112734013-d099ed80-8f4b-11eb-8336-2d50bc6fab54.png)
![eis1](https://user-images.githubusercontent.com/45431675/112734016-d42d7480-8f4b-11eb-9b0d-5f0ea4e63a59.png)

Let me know if you have ideas for additional basic functionality.

ToDo:
- [ ] Curve smoothing with [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter)
- [ ] Peak detection
- [ ] Dynamic baseline by using the first and second derivatives
- [ ] Method summary printout and experiment grouping
- [ ] % peak comparison printout for grouped experiments
