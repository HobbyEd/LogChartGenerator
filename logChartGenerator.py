import os, glob
import json
from os import listdir
from os.path import isfile, join
from pprint import pprint
import io
import time
import sys

# Import chart libaries
import plotly
import plotly.plotly as plotlyOnline
import plotly.graph_objs as plotlyChart


class LogChartPlotter: 
    logSeries = []  # contains all the log data that is aviable on disk
   
    def __init__(self):
        # first read in all the logFiles
        self.logSeries = self.loadLogFiles()

    # This function read the logfiles in the folder /Logs and return a dictionary with the JSON data
    def loadLogFiles(self):
        folderPath = "./logs"
        data = []
        # read all t he logfiles in the directory
        for filename in glob.glob(os.path.join(folderPath, '*.txt')):
            with io.open(filename, encoding='utf-16') as f:
                try:
                    fileTimeStamp = os.path.getmtime(filename)
                    buffer = json.load(f)
                    for logEntry in buffer: 
                        logEntry['timeStamp'] = fileTimeStamp
                    data.append(buffer)
                except Exception as e: 
                    print(str(e) + " " + filename) 
                finally:
                    f.close() 
     

        # write a temperory logfile 
        with io.open("log.txt", 'w', encoding='utf-16') as f:
            json.dump(str(data), f)
            f.close()
        return data
  
    # Resultats a dict with for a specific instanceName the log information. 
    def getTimeSerieOnInstanceName(self, instanceName): 
        logSerie = []
        for logInstance in self.logSeries: 
            for logKey in logInstance: 
                if (logKey["instanceName"] == instanceName):
                    logSerie.append(logKey)
        return logSerie

    # Results all the instanceNames and there id in a dict that are available in the log files
    def getCustomInstanceNamesandIDs(self): 
        traces = [] #A trace is a timeseries that will be plotted on the charged. 
        traces.append(self.generateTraceForPlotly("LRV 2017", "6d9b225a-6694-42a6-9797-6f690cbc00d0"))
        traces.append(self.generateTraceForPlotly("TVU-Hoofdrol 2017", "694ddfe7-597d-49f3-b188-e3fed692ba32"))
        traces.append(self.generateTraceForPlotly("TKV 2017", "678ddd79-87ca-4b9e-bc10-f7f41e7a0b13"))
        traces.append(self.generateTraceForPlotly("Beeld & Geluid 2017", "3ba41222-0823-4273-84c2-e5197f127636"))
        traces.append(self.generateTraceForPlotly("TVU-Hoofdrol 2015", "7232aee2-d650-4dba-b34e-82f00d552745"))
        traces.append(self.generateTraceForPlotly("Kleine geldstr. speech 2017", "a8737169-b5e6-497e-b94a-9b7b61526aa1"))
        traces.append(self.generateTraceForPlotly("TKV 2016", "0973ba5d-9f16-4341-8f2d-27db2ab3d3ed"))
        traces.append(self.generateTraceForPlotly("LRV 2016", "870c41bd-bf75-441a-96f6-4a4b2fda8083"))
        traces.append(self.generateTraceForPlotly("TKV 2015", "dbb5c4d9-2268-4a5b-ae18-3b80b2624d6d"))
        traces.append(self.generateTraceForPlotly("TVU-Hoofdrol 2016", "49fa47ab-c20a-4ea9-95b5-4eb118fa0175"))
        traces.append(self.generateTraceForPlotly("Beeld & Geluid", "ddb99103-9907-42fd-9ede-82f54c689e04"))
        traces.append(self.generateTraceForPlotly("Beeld & Geluid 2016", "b1474dba-8a22-4b32-a54e-5eb0132f6d66"))
        traces.append(self.generateTraceForPlotly("VOD 2015", "8d43312c-b37f-428f-adb7-3c0ee7385361"))
        traces.append(self.generateTraceForPlotly("Kleine geldstr. speech 2015", "3e6f84ad-53f9-4044-9ef0-d0049be8e72f"))
        traces.append(self.generateTraceForPlotly("Kleine geldstr. speech 2016", "ba07687f-3137-4943-b75e-42b8311c1c36"))
        return traces

    def generateTraceForPlotly(self, instanceName, instanceCode):
        logSerie = self.getTimeSerieOnInstanceName (instanceCode)
        queSize = []
        timeStamps =[]
        for logEntry in logSerie: 
             queSize.append(int(logEntry["rawValue"]))
             timeStamp = time.ctime(logEntry["timeStamp"])
             timeStamps.append(timeStamp)
        trace = plotlyChart.Scatter(
            x=timeStamps, 
            y=queSize, 
            mode = 'lines+markers',
            name = instanceName)
        return trace

    def generateChartPlotly(self, online):
        data = self.getCustomInstanceNamesandIDs()
        layout = dict(title = 'Te verwerken budgetrondes',
                  xaxis = dict(title = 'Tijd'),
                  yaxis = dict(title = 'Te verwerken commands'),
                  )
        fig = dict(data=data, layout=layout)
        if (online): 
            plotlyOnline.plot(fig, filename='styled-line', auto_open=True)
        else: 
            plotly.offline.plot(fig, filename='styled-line', auto_open=True)

if __name__ == "__main__": 
    plotter = LogChartPlotter()
    parameter = sys.argv
    #check whether there is added a parameter to the script. If not plot the chart offline
    if (len(parameter) == 1):
        print (" +++ The chart will be generated localy. To generate an online chart add a parameter 'online' in the Commandline")
        plotter.generateChartPlotly(False)
    elif (str.upper(parameter[1]) == "ONLINE"): 
        print (" +++ The chart will be generated online. To generate an offline chart remove the parameter.")
        plotter.generateChartPlotly(True)
    else: 
        print (" +++ Only the parameter 'online' is accepted. By default the chart is plotted offline")
