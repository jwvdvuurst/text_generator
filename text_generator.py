# Text Generator
from keras.models import Sequential
from keras.layers import Dense
import argparse
import os 
import glob
from os import path
from keras.engine.saving import model_from_json
import numpy as np

dsnum = 1;
dslines = 0;
inputs_processed = []

def load_from_datasets( model ):
    processed = []
    X = []
    Y = []

    if path.exists( "datasets_processed.csv" ):
        with open( "dataset_processed.csv", "r") as dp:
            line = dp.readline()
            if line:
                processed.append(line)
                line = dp.readline()

    dsfnum = 1
    dsname = "dataset"+str(dsfnum)+".csv"

    while (path.exists(dsname)):
        process = 0
        try:
            if not processed.index(dsname):
                process = 1
        except ValueError as e:
            print( "An exception occurred ", e )
            print( "For now it can be ignored ")
            
            process = 1

        if process == 1:
            print( "Going to process dataset "+dsname )
            dataset = np.loadtxt(dsname, delimiter=",")

            X = dataset[:,0:18]
            Y = dataset[:,18:24]

            # for d in dataset:
            #     X.append( d[0:18] )
            #     Y.append( d[18:6] )
             
            model.fit( X, Y, epochs=150, batch_size=10, verbose=0)
            scores = model.evaluate( X, Y, verbose=0)
            print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
            processed.append( dsname )
            print( "Done processing dataset "+dsname )

        dsfnum = dsfnum + 1
        dsname = "dataset"+str(dsfnum)+".csv"

    with open( "dataset_processed.csv", "w") as dp:
        for line in processed:
            dp.write( line + "\n" )
    
def setup():
    model = Sequential()
    model.add( Dense( 27, input_dim=18, activation='relu' ))
    model.add( Dense( 22, activation='relu'))
    model.add( Dense( 11, activation='relu'))
    model.add( Dense( 6, activation='sigmoid'))

    if path.exists( "model.json"):
        with open( "model.json") as json_file:
            model_json = json_file.read()

            loaded_model = model_from_json( model_json )
            if path.exists( "model.h5" ):
                loaded_model.load_weights("model.h5")
        
        model.compile( loss='binary_crossentropy', optimizer='adam' )

        load_from_datasets( model )

    else:        
        model = Sequential()
        model.add( Dense( 27, input_dim=18, activation='relu' ))
        model.add( Dense( 22, activation='relu'))
        model.add( Dense( 11, activation='relu'))
        model.add( Dense( 6, activation='sigmoid'))

        model.compile( loss='binary_crossentropy', optimizer='adam' )

        load_from_datasets( model )

        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write( model_json )
            model.save_weights( "model.h5" )


def learn_from( file ):
    global dsnum
    global dslines

    dsname = "dataset"+str(dsnum)+".csv"

    if path.exists( dsname ):
        dssize = path.getsize( dsname )

        #currently set maxsize to 4 MB
        if (( dssize < 4*1024*1024 ) and (dslines < 10000)):
            dataset = open( dsname, "w+")
        else:
            dsnum = dsnum + 1
            dsname = "dataset"+str(dsnum)+".csv"
            dataset = open( dsname, "w" )
            dslines = 0
    else:
        dataset = open( dsname, "w" )
        dslines = 0

    infile = open( file, "r" )

    lines = infile.readlines()

    inputs = []

    for ip in range(25):
        inputs.append( 0 )

    for line in lines:
        parts = line.split()

        words = parts[0].split("_")

        for w in range(3):
            for l in range(len(words[w])):
                index = (w*6)+l

                try:
                    if ((l==0) or (l==4)):
                        inputs[index] = (ord( words[w][l] ) - ord( "A" )) / 26;
                    elif (l==5):
                        if len(words[w]) == 7:
                            inputs[index] = ( int( words[w][5]+words[w][6] ) / 99 )
                        else:
                            inputs[index] = ( int( words[w][5] ) / 99 )
                    elif (l==6):
                        pass
                    else: inputs[index] = ( int( words[w][l]) / 9 )
            
                    if (w == 0):
                        if ((l==0) or (l==4)):
                            inputs[l+19] = (ord( parts[1][l] ) - ord( "A" )) / 26;
                        elif (l==5):
                            if len(parts[1]) == 7:
                                inputs[l+19] = ( int( parts[1][5]+parts[1][6] ) / 99 )
                            else:
                                inputs[l+19] = ( int( parts[1][5] ) / 99 )
                        elif (l==6):
                            pass
                        else: inputs[l+19] = ( int( parts[1][l]) / 9 )
                except IndexError as e:
                    print( "Exception occurred ", e )
                    print( "w: ",w, "l: ",l," index: ",index )
                    exit(1);
        
        dataline = ""
        for l in range(25):
            dataline = dataline + str( inputs[l] )

            if not l == 24:
                dataline = dataline + ", "

        dataline = dataline + "\n"

        dataset.write( dataline )
        dslines = dslines + 1

        if (dslines > 10000):
            dataset.close()
            dsnum = dsnum + 1
            dsname = "dataset"+str(dsnum)+".csv"
            dataset = open( dsname, "w" )
            dslines = 0

    dataset.close()

    print( "Processed file: " + file )

def learn():
    global inputs_processed

    number = 0

    if path.exists( "inputs_processed.csv" ):
        with open( "inputs_processed.csv", "r") as ip:
            inputs_processed = ip.readlines()
        
    for file in glob.glob( "inputs_*.txt"):
        if file not in inputs_processed:
            print( "Learning from file "+file )
            learn_from( file )
            inputs_processed.append(file)

            number = number + 1

            if number > 10:
                with open( "inputs_processed.csv", "w") as ip:
                    ip.writelines( "%s\n" % l for l in inputs_processed )
                number = 0    

    with open( "inputs_processed.csv", "w") as ip:
        ip.writelines( "%s\n" % l for l in inputs_processed )    

def clear(): 
    print( "Lets clear" ) 

def work():
    print( "Lets work" )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", help="Setup the neural network", action="store_true")
    parser.add_argument("--learn", help="Let the neural network learn", action="store_true" )
    parser.add_argument("--clear", help="Clears the neural network", action="store_true" )
    parser.add_argument("--work", help="Let the neural network work", action="store_true" )
    args = parser.parse_args()

    if args.setup:
        setup()

    if args.learn: 
        learn()

    if args.clear: 
        clear()

    if args.work: 
        work()

    print( "Done" )
