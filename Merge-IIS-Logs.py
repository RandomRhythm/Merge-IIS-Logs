#merge all IIS logs into one big file
import os
def mergeLogs(strInputFile, strOutputFile):
    global boolHeaderWritten
    f1 = open(strInputFile, 'r', encoding="utf-8")
    f2 = open(strOutputFile, 'a+', encoding="utf-8")
    for line in f1:
        if line[:1] == "#":
            if boolHeaderWritten == False:
                if line[:9] == "#Fields: ":
                    f2.write(line[9:]) #write header row
                    boolHeaderWritten = True
        else:    
            f2.write(line) #write log entry
    f1.close()
    f2.close()

strOutputPath = "IIS_Combined.log"
strInputPath = "D:\\IIS\LogFiles\\W3SVC2\\"
boolHeaderWritten = False
if os.path.isdir(strInputPath):
    for folder in os.listdir(strInputPath):
        if "W3SVC" in strInputPath: #merge just the one site
          for file in os.listdir(strInputPath):
            mergeLogs(os.path.join(strInputPath, file), strOutputPath)          
        else:  #merge all IIS access logs
          for file in os.listdir(strInputPath + "\\" + folder + "\\"):
              mergeLogs(os.path.join(strInputPath + "\\" + folder + "\\", file), strOutputPath)
