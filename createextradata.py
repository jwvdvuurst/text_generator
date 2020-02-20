from os import path
import numpy as np
import math

extradatasets = []
datasets = []

for l in range(10):
    emptylist = []
    extradatasets.append( emptylist )

for l in range(6333):
    datasets.append( "dataset"+str(l+1)+".csv" )

dsnumber = 0

while (len(datasets) > 0):
    dsn = math.floor(np.random.random() * len(datasets))
    
    dsname = datasets[dsn]
    del datasets[dsn]

    if path.exists(dsname):
        dsnumber = dsnumber + 1
        print( str(dsnumber)+": Reading dataset "+dsname+" ("+str(len(datasets))+" left) -> "+str(len(extradatasets[0]))+" samples " )
        with open( dsname, "r" ) as infile:
            lines = infile.readlines()
        
        number = 0
        while (number * 3000 + 9 < len(lines)):
            for l in range(10):
                extradatasets[l].append( lines[number * 3000 + l] )
            number = number + 1

for l in range(10):
    edsname="dataset"+str(7000+l)+".csv"

    with open( edsname, "w") as outfile:
        outfile.writelines( "%s\n" % line for line in extradatasets[l] )



