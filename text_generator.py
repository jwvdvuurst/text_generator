# Text Generator
import tf
from keras.models import Sequential
from keras.layers import Dense
import argparse
import os 
import glob

def setup():
    # tf.logging.set_verbosity(tf.logging.DEBUG)

    model = Sequential()
    model.add( Dense( 27, input_dim=18, activation='relu' ))
    model.add( Dense( 22, activation='relu'))
    model.add( Dense( 11, activation='relu'))
    model.add( Dense( 6, activation='sigmoid'))

    model.compile( loss='binary_crossentropy', optimizer='adam' )

def learn_from( file ):
    infile = open( file, "r" )

    lines = infile.readlines()

    inputs = []
    outputs = []

    for ip in range(18):
        inputs.append( 0 )

    for op in range(7):
        outputs.append( 0 )

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
                            outputs[l] = (ord( parts[1][l] ) - ord( "A" )) / 26;
                        elif (l==5):
                            if len(parts[1]) == 7:
                                outputs[l] = ( int( parts[1][5]+parts[1][6] ) / 99 )
                            else:
                                outputs[l] = ( int( parts[1][5] ) / 99 )
                        elif (l==6):
                            pass
                        else: outputs[l] = ( int( parts[1][l]) / 9 )
                except IndexError as e:
                    print( "Exception occurred ", e )
                    print( "w: ",w, "l: ",l," index: ",index )
                    exit(1);
        
        print( "File:    ", file )
        print( "Line:    ", line )
        print( "Inputs:  ", inputs )
        print( "Outputs: ", outputs ) 

def learn():
    for file in glob.glob( "inputs_*.txt"):
        print( "Learning from file "+file )
        learn_from( file )

def clear(): 
    print( "Lets clear" ) 

def work():
    print( "Lets work" )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--learn", help="Let the neural network learn", action="store_true" )
    parser.add_argument("--clear", help="Clears the neural network", action="store_true" )
    parser.add_argument("--work", help="Let the neural network work", action="store_true" )
    args = parser.parse_args()

    setup()

    if args.learn: 
        learn()

    if args.clear: 
        clear()

    if args.work: 
        work()

    print( "Done" )
