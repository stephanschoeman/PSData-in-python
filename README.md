# PSData in python
 Load a .pssession file into python for local processing.
 I do a bunch of [Cyclic Voltammetry](https://en.wikipedia.org/wiki/Cyclic_voltammetry) and [Square Wave Voltammetry](https://en.wikipedia.org/wiki/Squarewave_voltammetry) experiments regularly and wrote this Python script to extact my data for some post-processing. The main purpose is to skip additional export steps from the .pssession file, but I added plotting and baseline tools. I use [this](https://www.palmsens.com/product/palmsens4/) device for my measurements.
 
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

Create the data object that will contain all your experiment information. The object creation automatically load the data into the object:
```
data = PS.jparse(r'..\File.pssession')
```

You can then plot the data by using:
```
data.plot()
```

and that is about all you need to get started!

**Additional functionality (so far):**
- ```data.methodFilter = data.methodType.SWV``` will filter all plots on SWV. Also available: CV and EIS
- ```data.baseline``` (only available for SWV):
  - ```.startPosition``` set to int value of the position that you want to use for the baseline. Must be set for baseline to work.
  - ```.endPosition``` set to int value of the position that you want to use for the baseline. If not set, taken as ```len(measurements) - startPosition```
- ```.experimentList``` gives you all of the tags for the experimets that are in the object.
- ```.plot(['SWV 1','CV 1'])``` or ```.plot([data.experimentList[0],data.experimentList[5]])``` will only plot the experiments with these tags. The plot legend also contains the experiment tags.

**Example plots:**

Here is a raw SWV experiment plot:

![SWV Raw](https://drive.google.com/uc?export=view&id=1cSfbIJnPDbMwvZKf04IyDE6yvJHXTZba)

and then I did a baseline subtraction on starting position 7:

![SWV Baseline](https://drive.google.com/uc?export=view&id=1bp-EswtDpwZAEcG7yr4WBwHFOkk-176E)

Here is an example of an EIS measurement plot:

![EIS Raw](https://drive.google.com/uc?export=view&id=1-HvuJfHDtJeVflLOh3hmkf1RPH5pqiqc)

Let me know if you have ideas for additional basic functionality.

ToDo:
- [ ] Curve smoothing with [Savitzky–Golay filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter)
- [ ] Peak detection
- [ ] Dynamic baseline by using the first and second derivatives
- [ ] Method summary printout and experiment grouping
- [ ] % peak comparison printout for grouped experiments
