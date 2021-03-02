# PSData in python
 Load a .pssession file into python for local processing.
 I do a bunch of [Cyclic Voltammetry](https://en.wikipedia.org/wiki/Cyclic_voltammetry) and [Square Wave Voltammetry](https://en.wikipedia.org/wiki/Squarewave_voltammetry) experiments regularly and wrote this Python script to extact my data for some post-processing. The main purpose is to skip additional export steps from the .pssession file, but I added plotting and baseline tools. I use [this](https://www.palmsens.com/product/palmsens4/) device for my measurements.
 
 **Supported experiments:**
 - Square wave voltammetry (primary)
 - Cyclic voltammetry
 - Electrical impedance spectroscopy
 
 **Get started:**
 
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

Import PSData:
```
import PSData as PS
```

Create the data object that will contain all your experiment information. The object creation automatically loads the data into the object:
```
data = PS.jparse([r'..\File.pssession'])
```
Note that the input requires an array for the file locations.

You can then plot the data by using:
```
data.plot()
```

and that is about all you need to get started!

**Additional functionality:**
- ```data.methodFilter = data.methodType.SWV``` will filter all plots on SWV. Also available: CV and EIS
- ```data.baseline``` (only available for SWV):
  - ```.startPosition``` set to int value of the position that you want to use for the baseline. Must be set for baseline to work.
  - ```.endPosition``` set to int value of the position that you want to use for the baseline. If not set, taken as ```len(measurements) - startPosition```
- ```.experimentList``` gives you all of the tags for the experimets that are in the object.
- ```.plot(['SWV 1','CV 1'])``` or ```.plot([data.experimentList[0],data.experimentList[5]])``` will only plot the experiments with these tags. The plot legend also contains the experiment tags.
- ```.eisTypes.scale = 1000``` sets the scale of the Nyquist plot. Usable scales: k, M, G, T. You can expand this list as required.
- The datapoints within the experiments are stored in a dictionary ```.datapoints```. This can be accessed via the experiments labels ```data.datapoints[data.experimentList[0]]``` or ```data.datapoints['CV 1']```. EIS data is stored in an EIS object and has a few different tags, while all other measurements are stored in an axis object with xvalues and yvalues:
  - EIS phase, for example: ```data.datapoints[data.experimentList[i]]['-Phase']``` You can view the EIS tags within the ```.eisTypes``` object.
  - X-axis values for all other: ```data.datapoints[data.experimentList[i]].xvalues```
- You can process multiple files at once:
  - When creating the PSData object, place the file locations as an array when parsing: ```data = PS.jparse([r'floc\file1.pssession', r'floc\file2.pssession'])```
  - The results will be grouped by their units and plotted together, but you can disable this by setting ```data.splitGraphs = False```
  - The data is parsed seperately into different objects, so a dictionary of these objects are created based on the file names: ```data.data['A']``` will give you access to the PSData object of file A.pssession. The ```data.datapoints[]``` is still accessible without having to reference the filenames.
  - The tags of the experiments continue between files. So if A contains 3xSWV and B contains 2xSWV and 2XCV, the tag list will be: ```[SWV 1, SWV 2, SWV 3, SWV 4, SWV 5, CV 1, CV 2]```
- Graph titles: ```.titles = ['All unfiltered SWV data', 'CV unfiltered', 'Nyq', 'ZvsZdash']``` is an example of setting the graph titles. The order is important, so run it once to check in which order the graphs are shown. The amount of required titles are calculated when you set the ```.titles``` array, and it will print out the required title count if you have insufficient/too many titles.

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
