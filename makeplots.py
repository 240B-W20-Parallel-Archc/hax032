#!/usr/bin/env python2.7
import re

import numpy as py
import matplotlib
matplotlib.use('pdf')
# from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

#
# plotOneSeries
#
def plotOneSet(rawData, sName, col='r'):
    sz = []
    lat = []
    for l in rawData:
        m = re.search('size:\s+(\d+)\s*K?\s+latency:\s+(\d+\.\d+)\sns', l)
        if (m):
            csz = int(m.group(1))
            if re.search('\d+\s+K\s+latency', l):
                csz = 1024 * csz
            sz.append(csz)
            lat.append(float(m.group(2)))

    plt.plot(sz, lat, label=sName, marker='o', linestyle='dashed', c=col)
    plt.legend(loc='upper left')
#    plot.show()
    

#
# finalizePlot
def finalizePlot(plotfilename):
    plt.xscale('log')
    plt.savefig(plotfilename+".pdf")

#
# def doPlot
#   rawData is the output of the cachetime  program
def doPlot(rawData, plotfilename):
    plotOneSet(rawData, plotfilename)
    finalizePlot(plotfilename)
    sz = []
    lat = []
    for l in rawData:
        m = re.search('size:\s+(\d+)\s*K?\s+latency:\s+(\d+\.\d+)\sns', l)
        if (m):
            csz = int(m.group(1))
            if re.search('\d+\s+K\s+latency', l):
                csz = 1024 * csz
            sz.append(csz)
            lat.append(float(m.group(2)))

    print sz
    print lat
    for x,y in zip(sz, lat):
        print("{:d}, {:f}".format(x,y))


    plt.plot(sz, lat)
    plt.xscale('log')
#     pp = PdfPages('multipage.pdf')
#    plt.savefig(pp, format='pdf')
#    pp.close()
    plt.savefig(plotfilename)
#    plot.show()

#
#
if __name__ == "__main__":
    import sys
    fp = ""

    cols = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    colIdx = 0
    for fname in sys.argv[1:]:
        try:
            fp = open(fname, "r")
        except:
            print("Error: Could not open file {:s}".format(fname))
            exit(-1)


        plotOneSet(fp.readlines(), fname, cols[colIdx])
        colIdx = colIdx + 1

    finalizePlot("_".join(sys.argv[1:]))
