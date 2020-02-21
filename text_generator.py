# Text Generator
from keras.models import Sequential
from keras.layers import Dense
import argparse
import os 
import glob
from os import path
from keras.engine.saving import model_from_json
import numpy as np
from numpy import random
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

dsnum = 1;
dslines = 0;
inputs_processed = []

def create_model():
    model = Sequential()
    model.add( Dense( 18, input_dim=18, activation="sigmoid"))
#    model.add( Dense( 27, input_dim=18, activation='relu' ))
    model.add( Dense( 18, activation="sigmoid"))
    model.add( Dense( 36, activation="sigmoid"))
    model.add( Dense( 72, activation="sigmoid"))
    model.add( Dense(144, activation="sigmoid"))
    model.add( Dense( 102, activation="sigmoid"))
    model.add( Dense( 51, activation="sigmoid"))
    model.add( Dense( 26, activation="sigmoid"))
    model.add( Dense( 13, activation="sigmoid"))
    model.add( Dense( 6, activation="sigmoid"))            
    # model.add( Dense( 27, activation='relu'))
    # model.add( Dense( 27, activation='sigmoid'))
    # model.add( Dense( 22, activation='relu'))
    # model.add( Dense( 22, activation='relu'))
    # model.add( Dense( 22, activation='sigmoid'))
    # model.add( Dense( 11, activation='relu'))
    # model.add( Dense( 11, activation='relu'))
    # model.add( Dense( 11, activation='sigmoid'))
    # model.add( Dense( 6, activation='relu'))
    # model.add( Dense( 6, activation='sigmoid'))

    model.compile( loss='binary_crossentropy', optimizer='adam' )

    return model

def save_model( model ):
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write( model_json )
        model.save_weights( "model.h5" )

def load_model():
    model = create_model()
    model.load_weights( "model.h5" )

    model.compile( loss='binary_crossentropy', optimizer='adam' )

    return model

def load_from_datasets( model ):
    datasets = []
    processed = []
    X = []
    Y = []

    if path.exists( "datasets_processed.csv" ):
        with open( "dataset_processed.csv", "r") as dp:
            line = dp.readline()
            if line:
                processed.append(line)
                line = dp.readline()

    for l in range(10):
        dsname = "dataset"+str(7000+l)+".csv"

        if path.exists(dsname):
            print( "Going to deep process dataset "+dsname )
            dataset = np.loadtxt(dsname, delimiter=",")

            X = dataset[:,0:18]
            Y = dataset[:,18:24]

            # for d in dataset:
            #     X.append( d[0:18] )
            #     Y.append( d[18:6] )
             
            model.fit( X, Y, epochs=100, batch_size=25, verbose=0)
            scores = model.evaluate( X, Y, verbose=0)
            print( "scores ", scores)
            # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
            processed.append( dsname )
            print( "Done processing dataset "+dsname )
            
    save_model( model )

    for l in range(6333):
        datasets.append( "dataset"+str(l)+".csv" )

    for l in range(10):
        datasets.append( "dataset"+str(7000+l)+".csv" )

    dsn = 0

    while (len(datasets) > 0):
        dsfnum = math.floor( random.random() * len(datasets) )
        dsname = datasets[dsfnum]
        del datasets[dsfnum]
        dsn = dsn + 1

        if (path.exists(dsname)):
            process = 0
            try:
                if not processed.index(dsname):
                    process = 1
            except ValueError as e:            
                process = 1

            if process == 1:
                print( "Going to process dataset "+dsname )
                dataset = np.loadtxt(dsname, delimiter=",")

                X = dataset[:,0:18]
                Y = dataset[:,18:24]

                # for d in dataset:
                #     X.append( d[0:18] )
                #     Y.append( d[18:6] )
             
                model.fit( X, Y, epochs=10, batch_size=25, verbose=0)
                scores = model.evaluate( X, Y, verbose=0)
                print( "scores ", scores)
                # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
                processed.append( dsname )
                print( "Done processing dataset "+dsname )


        if (dsn % 10 == 0):
            save_model( model )
            with open( "dataset_processed.csv", "w") as dp:
                dp.writelines("%s\n" % l for l in processed )
    
    with open( "dataset_processed.csv", "w") as dp:
        dp.writelines("%s\n" % l for l in processed )

    
def setup():
    model = create_model()

    if path.exists( "model.json"):
        with open( "model.json") as json_file:
            model_json = json_file.read()

            loaded_model = model_from_json( model_json )
            if path.exists( "model.h5" ):
                loaded_model.load_weights("model.h5")
        
        model.compile( loss='binary_crossentropy', optimizer='adam' )

        load_from_datasets( model )

    else:        
        model = create_model()

        load_from_datasets( model )

        save_model( model )

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

def soundex(word):
        
    codes = ["bfpvw","cgjhkqsxz", "dt", "l", "mn", "r"]
   
    sdx=word[0].upper()
    pc="9"
    cc="9"
    for l in word[1:].lower():
        i=0
        for code in codes:
            if l in code:
                cc = str(i+1)
            i += 1
    
        if cc.isdecimal():
            if cc != '9' and cc != pc:
                sdx = sdx + cc
                pc = cc
    
    sdx = sdx + "000"
    sdx = sdx[0:4]
    sdx = sdx + word[-1].upper()+str(len(word))
    return sdx

def encode_inputs( words ):
    X = []

    for ws in words:
        t = []
        t.append( soundex( ws[0] ) )
        t.append( soundex( ws[1] ) )
        t.append( soundex( ws[2] ) )

        TXs = []

        for w in range(3):
            for l in range(len(t[w])):
                index = (w*6)+l

                try:
                    if ((l==0) or (l==4)):
                        TXs.append((ord( t[w][l] ) - ord( "A" )) / 26)
                    elif (l==5):
                        if len(t[w]) == 7:
                            TXs.append( int( t[w][5]+t[w][6] ) / 99 )
                        else:
                            TXs.append( int( t[w][5] ) / 99 )
                    elif (l==6):
                        pass
                    else: TXs.append( int( t[w][l]) / 9 )
                except IndexError as e:
                    print( "Exception occurred ", e )
                    print( "w: ",w, "l: ",l," index: ",index )
                    TXs.append(0.0)
        
        X.append( TXs )

    return X            

def decode_outputs( Y ):
    return Y

def work():
    if ( path.exists( "model.json" ) and path.exists( "model.h5" ) ):
        model = load_model()

        words = [["in", "de", "ochtend"], ["wakker", "worden", "zonder"], ["jouw", "lichaam", "naast"], ["in", "de", "negentiende"], ["hitler", "was", "een"],
                 ["de", "ster", "in"], ["hij", "dwaalde", "met"], ["python", "is", "een"], ["python", "is", "a"], ["what", "makes", "someone"]]

        print( "Work: words of input: ", words)
        print( "Work: with length ",len(words))

        Xnew = np.asarray( encode_inputs( words ) )

        print( "Work: encoded words into ", Xnew )
        print( "Work: with length ",len(Xnew))
        
        Ynew = model.predict( Xnew )

        answers = decode_outputs( Ynew )

        if len( Xnew ) == len( answers ):
            for l in range( len( Xnew )):
                ws = words[l]
                print( "Based upon the input ", Xnew[l] )
                print( "Answer predicted: ", answers )
                print( ws[0] + " " + ws[1] + " " + ws[2] + " : " + str(answers[l]) )
        else:
            print( words )
            print( answers ) 


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
