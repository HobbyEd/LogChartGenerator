import os, glob
import json
from os import listdir
from os.path import isfile, join
from pprint import pprint
import io
import time

#Import chart libaries
import plotly
import plotly.plotly as plotlyOnline
import plotly.graph_objs as plotlyChart

# This function read the logfiles in the folder /Logs and return a dictionary with the JSON data
def loadLogFiles():
    folderPath = "./logs"
    data = []
    #read all t he logfiles in the directory
    for filename in glob.glob(os.path.join(folderPath, '*.txt')):
        with io.open(filename, encoding='utf-16') as f:
            fileTimeStamp = os.path.getmtime(filename)
            buffer = json.load(f)
            for logEntry in buffer: 
                logEntry['timeStamp'] = fileTimeStamp
            data.append(buffer)
            f.close() 

    #write a temperory logfile 
    with io.open("log.txt", 'w', encoding='utf-16') as f:
        json.dump(str(data), f)
        f.close()
    return data

def getTimeSerieOnInstanceName(instanceName): 
    #first read in all the logFiles
    data = loadLogFiles()
    logSerie = []
    for logInstance in data: 
        for logKey in logInstance: 
            if (logKey["instanceName"] == instanceName):
                logSerie.append(logKey)
    return logSerie


def generateTraceForPlotlyOnline(instanceName, instanceCode):
    logSerie = getTimeSerieOnInstanceName (instanceCode)
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

def generateChartPlotly(online):
    trace0 = generateTraceForPlotlyOnline("LRV 2017", "6d9b225a-6694-42a6-9797-6f690cbc00d0")
    trace1 = generateTraceForPlotlyOnline("TVU-Hoofdrol 2017", "694ddfe7-597d-49f3-b188-e3fed692ba32")
    trace2 = generateTraceForPlotlyOnline("LRV 2017 (2)", "7232aee2-d650-4dba-b34e-82f00d552745")
    trace3 = generateTraceForPlotlyOnline("TKV 2017", "678ddd79-87ca-4b9e-bc10-f7f41e7a0b13")
    trace4 = generateTraceForPlotlyOnline("Beeld & Geluid 2017", "3ba41222-0823-4273-84c2-e5197f127636")
    trace5 = generateTraceForPlotlyOnline("Kleine geldstr. speech 2017", "a8737169-b5e6-497e-b94a-9b7b61526aa1")
    data =[trace0, trace1, trace2,trace3, trace4, trace5]
    layout = dict(title = 'Te verwerken budgetrondes',
              xaxis = dict(title = 'Tijd'),
              yaxis = dict(title = 'Te verwerken commands'),
              )
    fig = dict(data=data, layout=layout)
    if (online): 
        plotlyOnline.plot(fig, filename='styled-line', auto_open=True)
    else: 
        plotly.offline.plot(fig, filename='styled-line', auto_open=True)

generateChartPlotly(True)
