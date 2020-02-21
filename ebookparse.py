import pathlib
from pathlib import Path

import ebooklib
from ebooklib import epub

import os
import shutil
import re
from lxml import etree 
from zipfile import ZipFile, BadZipFile


ebookspath=pathlib.Path("C:/Users/John/books")
temppath=pathlib.Path("C:/Users/John")
tempname="temp.epub"
tempfilename=os.path.join( temppath, tempname )


def copyepub( oldfile, newfile ):
    shutil.copy( oldfile, newfile )


def processbook( language, book ):
    countwords = {}
    nextwords = {}
    threegram = []

    def processword( word ):
        word = word.lower()
        if word in countwords.keys():
            countwords[word] += 1
        else:
            countwords[word] = 1
    
        if len(threegram) == 3:
            tgkey = threegram[0]+" "+threegram[1]+" "+threegram[2]
            if tgkey in nextwords.keys():
                if word in nextwords[tgkey].keys():
                    nextwords[tgkey][word] += 1
                else:
                    nextwords[tgkey][word] = 1
            else:
                nextwords[tgkey] = {}
                nextwords[tgkey][word] = 1
    
        threegram.append(word)

        if len(threegram) == 4:        
            threegram.pop(0)


    try:
        title=book.get_metadata( 'DC', 'title' )[0][0]
        print( "Title found ",title)
        title=re.sub( r'[\ \(\)\[\]\_\-\:\.\,\"\'\{\}\\\/\|\#\@\!\?\<\>\;\*\&\t\n]', '', title ).lower()
    except (AttributeError, TypeError, KeyError, FileNotFoundError, ebooklib.epub.EpubException ) as e:
        print( "Creating filename from title failed",e)
        return
    
    letter=title[:1].upper()
    pb_filename=letter+"\\"+language+"_"+title+".txt"
    print( "Creating file "+pb_filename+" for book "+title )
    if not os.path.exists( pb_filename ):
        with open( pb_filename, 'w' ) as file:
            try:
                regex = re.compile( r'^[A-Za-z]*$')
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        content = item.get_content()
                        for w in content.split():
                            if isinstance(w,bytes):
                                try:
                                    w = w.decode( "utf-8" )
                                    w = re.sub( r'\.\,\:\"\'\(\)\;\?\!', ' ', w)
                    
                                    if regex.match(w):                        
                                        processword(w)                                
                                except UnicodeDecodeError as e:
                                    print( "Unable to decode byte string ",e, "skipping word. \'n")
                                                                
                print( "Unique words: ",len(countwords), "Number of threegrams: ",len(nextwords),"\n")

                if len(countwords) > 0:
                    wl=list(countwords.keys())[len(countwords)-1]
                    wc=countwords[wl]
                    print( "Last word: ",wl," with count ",wc,"\n")
                if len(nextwords) > 0:
                    tgl=list(nextwords.keys())[len(nextwords)-1]
                    tgc=nextwords[tgl]
                    print( "last threegram: ", tgl, ": ",nextwords[tgl],"\n")

                sorted_words={k:v for k, v in sorted( countwords.items(), key=lambda item: item[1])}
            
                for sw in sorted_words.keys():
                    file.write( sw+" : "+str(sorted_words[sw])+"\n")

                for nw in nextwords.keys():
                    for nnw in nextwords[nw].keys():
                        file.write( nw+" -> "+nnw+" : "+str(nextwords[nw][nnw])+"\n")

                print( "Written file ", pb_filename )

            except (AttributeError, TypeError, KeyError, IndexError, FileNotFoundError, ebooklib.epub.EpubException ) as e:
                print( "processing of book failed.",e)
    
    else:
        print( "Skipped book, file "+pb_filename+" already exists.\n")



# def processbook( book ):
#     owl=len(countwords)
#     otg=len(nextwords)
#     nw=0
#     try:
#         regex = re.compile( r'^[A-Za-z]*$')
#         for item in book.get_items():
#             if item.get_type() == ebooklib.ITEM_DOCUMENT:
#                 content = item.get_content()
#                 for w in content.split():
#                     if isinstance(w,bytes):
#                         w = w.decode( "utf-8" )

#                     w = re.sub( r'\.\,\:\"\'\(\)\;\?\!', ' ', w)
                    
#                     if regex.match(w):                        
#                         processword(w)
#                         nw += 1
        
#         print( "Unique words: ",len(countwords), "Number of threegrams: ",len(nextwords),"\n")
#         print( "Number words in last book ", nw )
#         print( "New unique words found: ", len(countwords)-owl )
#         print( "New threegrams found: ",len(nextwords)-otg)

#         if len(countwords) > 0:
#             wl=list(countwords.keys())[len(countwords)-1]
#             wc=countwords[wl]
#             print( "Last word: ",wl," with count ",wc,"\n")
#         if len(nextwords) > 0:
#             tgl=list(nextwords.keys())[len(nextwords)-1]
#             tgc=nextwords[tgl]
#             print( "last threegram: ", tgl, ": ",nextwords[tgl],"\n")

#     except (AttributeError, TypeError, KeyError, ebooklib.epub.EpubException ) as e:
#         print( "processing of book failed.",e)
    


def parseepub( filename ):
    print( "Parse epub for file ", filename )
    try:
        book = epub.read_epub( filename )

        try:
            language = book.get_metadata('DC','language')
            if language == [('nl', {})]:
                print( "processing Dutch book: ", filename )
                processbook( "NL", book )
            elif language == [('en',{})]:
                print( "processing English book: ", filename )
                processbook( "EN", book )

        except (AttributeError, TypeError, KeyError, IndexError, FileNotFoundError, ebooklib.epub.EpubException, etree.XMLSyntaxError, BadZipFile) as e:
            print( filename, "Error occurred while reading metadata ", e)        
            

    except (AttributeError, TypeError, KeyError, IndexError, FileNotFoundError, ebooklib.epub.EpubException, etree.XMLSyntaxError, BadZipFile) as e:
        print( filename, "Error occurred while opening epub", e)
        

            
    

    

    


if __name__ == "__main__":      
    #find epub files under the directory ebookspath
    for l in "xXyYzZ0123456789":        
        for filename in Path( ebookspath ).rglob( l+'*.epub' ):
            parseepub( filename )