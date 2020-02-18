from itertools import groupby
import os
import fnmatch

dictionary = {}
inputs = {}
  
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

def process_file( filename ):
    infile = open( filename, "r" )
    lines = infile.readlines()
    for line in lines:
        words = line.split()
        if len( words ) == 7:
            if words[3] == "->":
                sw=['','','','','']
                i=0
                while( i < 5 ):
                    if i != 3:
                        sw[i] = soundex(words[i])
                        if sw[i] not in dictionary.keys():
                            # print( words[i] + " = " + sw[i] )
                            dictionary[sw[i]] = words[i]
                        else:
                            if type(dictionary[sw[i]]) is list:
                                if words[i] not in dictionary[sw[i]]:
                                    dictionary[sw[i]].append( words[i] )
                                    # print ( dictionary[sw[i]] )
                            else:
                                if words[i] != dictionary[sw[i]]:
                                    temp = dictionary[sw[i]]
                                    dictionary[sw[i]] = [ temp, words[i] ]
                                    # print ( dictionary[sw[i]] )
                    i += 1
               
                wordindex = sw[0] + "_" + sw[1] + "_" + sw[2]
                
                if wordindex not in inputs.keys():
                    # print( sw[0] + " " + sw[1] + " " + sw[2] + " : " + sw[4] + "// " + words[0] + " " + words[1] + " " + words[2] + " " + words[4] )                     
                    inputs[wordindex] = sw[4]
                else:
                    if type(inputs[wordindex]) is list:
                        if sw[4] not in inputs[wordindex]:
                            inputs[wordindex].append( sw[4] )
                            # print( sw[0] + " " + sw[1] + " " + sw[2]  + " : " + sw[4] + " added to list " )
                    else:
                        if inputs[wordindex] != sw[4]:
                            temp = inputs[wordindex]
                            inputs[wordindex] = [ temp, sw[4] ]
                            # print( sw[0] + " " + sw[1] + " " + sw[2] + " : " + sw[4] + " converted to list " )
                
def process_files_starting_with( section, letters ):
    for l in letters:
        path="texts\\"+l+"\\"
        with os.scandir( path ) as files:
            for f in files:
                process_file(path+f.name)
                print( "Processed file "+f.name )
                print( "dict: " + str( len( dictionary )))
                print( "inputs: " + str( len( inputs )))
    
    outfn = "inputs"+str(section)+".dat"
    with open( outfn, "w" ) as outfile:
        for ikey in inputs.keys():
            if type(inputs[ikey]) == list:
                for nw in inputs[ikey]:
                    outfile.write( ikey + " " + nw + "\n" )
            else:
                outfile.write( ikey + " " + inputs[ikey] + "\n" )
    inputs.clear()
                
def write_dictionary():
    outfn = "dictionary.dat"
    with open( outfn, "w" ) as outfile:
        for dkey in dictionary.keys():
            if type( dictionary[dkey] ) == list:
                for dentry in dictionary[dkey]:
                    outfile.write( dkey + " " + dentry + "\n" )
            else:
                outfile.write( dkey + " " + dictionary[dkey] + "\n" )
    
process_files_starting_with( 1, "ABCDEF" )
process_files_starting_with( 2, "GHIJKL" )
process_files_starting_with( 3, "MNOPQR" )
process_files_starting_with( 4, "STUVWX" )
process_files_starting_with( 5, "YZ0123" )
process_files_starting_with( 6, "456789" )

write_dictionary()
