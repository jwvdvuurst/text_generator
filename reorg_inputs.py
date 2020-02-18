maxlines=30000


for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    print( "Processing for lines starting with "+l )
    section=0
    counter=0
    outfn="inputs_"+l+str(section)+".txt"
    outfile=open( outfn, "w" )
    for i in "123456":
        infn="inputs"+i+".txt"
        infile=open( infn, "r" )
        
        lines=infile.readlines()
        for line in lines:
            if line[0] == l:
                outfile.write( line )
                counter += 1
                
                if counter > maxlines:
                    print( "Max number of lines reached for "+l+" switching... " )
                    print( "Last line written to "+outfn+" : "+line )
                    outfile.close()
                    section += 1
                    counter=0
                    outfn="inputs_"+l+str(section)+".txt"
                    outfile=open( outfn, "w" )

        infile.close()
        print( "processed inputs"+i+".dat --> until now "+str(counter)+" "+l+" records ")

outfile.close()