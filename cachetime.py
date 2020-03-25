#!/usr/bin/env python2.7
#!/usr/bin/python2.7
#!/opt/python/bin/python2.7

import time
import argparse
import subprocess
# import makeplots

#
# handle input args
#
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', type=int, default='1')
parser.add_argument('-s', '--sequential', action='store_true')
parser.add_argument('-r', '--random', action='store_true')
parser.add_argument('-m', '--modify', action='store_true')
parser.add_argument('--test', action='store_true')
parser.add_argument('-p', '--plot', action='store_true') 
parser.add_argument('minLg2', type=int, help="lg2 of the lower data array size")
parser.add_argument('maxLg2', type=int, help="lg2 of the upper data array size")
parser.add_argument('outnm', type=str, default="cachetime2.out",
                    help="output file root name")

args = parser.parse_args()

reps = 0
raw_output = []
for i in range(args.minLg2, args.maxLg2+1):
    if i < 12:
	if args.modify:
        	reps = 1000000000   # 1 B
	else:
        	reps = 10000000000   # 10 B
    elif i < 16:
	if args.modify:
        	reps = 100000000   # 100M
	else:
        	reps = 1000000000   # 1B
    else:
	if args.modify:
        	reps = 100000000   # 10M 
	else:
        	reps = 1000000000   # 100M 

    if args.test:
        reps = 10000

    startTime = 0
    endTime = 0

    if not args.sequential and not args.random:
        args.random = True

    if args.sequential:
        seqOrRand = '-s'
    else:
        seqOrRand = '-r'


    cpus = range(args.threads)
    cpus = [str(x) for x in cpus]
    cpus = ",".join(cpus)
    cpus = str(cpus)
    cmd = ['taskset', '-c', cpus]

    cmd.extend(['./cachetime', seqOrRand, str(reps)])
    if args.modify:
        cmd.append('-m')
    if args.threads:
        cmd.append('-t')
        cmd.append(str(args.threads))
    cmd.append(str(i))

#    print cmd
    try:
        startTime = time.time()
        raw_output.append(subprocess.check_output(cmd))
        endTime = time.time()
    except:
        print("Error: running cachetime")
        exit(-1)


    if ((endTime-startTime) < 10.0):
        print("Warning: time < 10.0 seconds {:f}".format(endTime-startTime))

try:
    fout = open(args.outnm+".txt", "w")
except:
    print("Error: Could not open otuput file {:s}".format(args.outnm))
    exit(-1)

for x in raw_output:
    fout.write(x)

fout.close()

if (args.plot):
    import makeplots
    makeplots.doPlot(raw_output, args.outnm)
