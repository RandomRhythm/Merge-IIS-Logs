#merge all IIS logs into one big file
import os
import sys
from optparse import OptionParser

def build_cli_parser():
    parser = OptionParser(usage="%prog [options]", description="Merge IIS logs")
    parser.add_option("-i", "--input", action="store", default=None, dest="InputPath",
                      help="Path to folder containing logs to be merged")
    parser.add_option("-o", "--output", action="store", default=None, dest="OutputPath",
                      help="Log output folder path")
    return parser

def mergeLogs(strInputFile, strOutputFile):
    global boolHeaderWritten
    f1 = open(strInputFile, 'r', encoding="utf-8")
    f2 = open(strOutputFile, 'a+', encoding="utf-8")
    columnCount = 0
    newColumnCount = 0
    newFileCount = 0
    for line in f1:
        if line[:1] == "#":
            newColumnCount = len(line[9:].split(" "))
            if boolHeaderWritten == False or newColumnCount > 4 and newColumnCount != columnCount:
                if line[:9] == "#Fields: ":
                    if newColumnCount > 4 and newColumnCount != columnCount and columnCount != 0: #change in column count
                        #change file path for output to new file
                        f2 = open(strOutputFile + str(newFileCount), 'a+', encoding="utf-8")
                        newFileCount +=1
                    f2.write(line[9:]) #write header row
                    boolHeaderWritten = True
                    columnCount = newColumnCount
        else:    
            
            f2.write(line) #write log entry
    f1.close()
    f2.close()

strOutputPath = "" #"IIS_Combined.log"
strInputPath = "" #"D:\\IIS\LogFiles\\W3SVC2\\"
parser = build_cli_parser()
opts, args = parser.parse_args(sys.argv[1:])
if opts.InputPath:
    strInputPath = opts.InputPath
    print (strInputPath)
if opts.OutputPath:
    strOutputPath = opts.OutputPath
    print (strOutputPath)
if not strInputPath or not strOutputPath:
    print ("Missing required parameter")
    sys.exit(-1)

boolHeaderWritten = False
if os.path.isdir(strInputPath):
    if "W3SVC" in strInputPath: #merge just the one site
        for file in os.listdir(strInputPath):
          mergeLogs(os.path.join(strInputPath, file), strOutputPath)
        exit()
    for folder in os.listdir(strInputPath):            
        if "W3SVC" in folder: #merge multiple sites
          subDir = os.path.join(strInputPath, folder)
          for file in os.listdir(subDir):
            mergeLogs(os.path.join(subDir, file), strOutputPath)          
        
