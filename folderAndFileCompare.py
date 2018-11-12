#!

# This script compares the contents of two linux folders (directories)
# It checks to see :
#  1. Are the contents in one the same as the conents in the other
#  2. Where the same file exists in both it checks for differences in these files - where differences are found a representation of the differences are created in HTML format and sotried in a 'comparisonHtmls' sub-folder
# The script also creates a log file with a summary of the comparison analysis.
#
# To run just type "python folderAndFileCompare.py" at the prompt where this file resides 

import difflib
import os
import datetime
import filecmp
import subprocess

def compareFile(firstFile, secondFile, diffFile, outputFile):
   if filecmp.cmp(firstFile,secondFile):
      outputFile.write("No changes detected between " + firstFile + " and " + secondFile + ".\n")
   else:
      firstFileLines = open(firstFile).readlines()
      secondFileLines = open(secondFile).readlines()
      difference = difflib.HtmlDiff().make_file(firstFileLines, secondFileLines, firstFile, secondFile)
      differenceReport = open(diffFile,'w')
      differenceReport.write(difference)
      differenceReport.close()
      outputFile.write("Changes detected between " + firstFile + " and " + secondFile + " have been written to " + diffFile + "\n")
      

def fileCheck(origFileName, compareFileName, bareFileName, comparisonDir, outputFile):
   try:
      f = open(compareFileName)
      f.close()
      #run a dos2unix on both files just in case one file originated in dos
      os.system("dos2unix " + str(origFileName))
      os.system("dos2unix " + str(compareFileName))
     
      #outputFile.write("File " + compareFileName + " exists. So compare next with original " + origFileName + "....\n")
      diffFile = comparisonDir + "/" + bareFileName + ".html"
      compareFile(origFileName, compareFileName, diffFile, outputFile)
      
   except IOError:
      #print('File ' + fileName + ' not found or not accessible')
      outputFile.write('File ' + compareFileName + ' not found or not accessible\n')


   
def printAndCompareFiles(origDir1, dir1, dir2, comparisonDir, outputFile):
   #print "Directory: ", dir1
   outputFile.write("Directory: " + dir1 + "\n")
   compareDir = dir1.replace(origDir1,dir2)
   
   for each in os.listdir(dir1):
      if os.path.isfile(os.path.join(dir1, each)):
         #print each
         #outputFile.write(each + "\n")
         fileCheck(os.path.join(dir1, each), compareDir + "/" + each, each, comparisonDir, outputFile )
      else:
         #print each + " is a dir, so recurse"
         printAndCompareFiles(origDir1, os.path.join(dir1, each), dir2, comparisonDir, outputFile)

input_dir1 = input("Input Directory:")
input_dir2 = input("Input Comparision Directory:")

whatTimeIsItMrWolf = str(datetime.datetime.now())
comparisonDir = "./comparisonHtmls" + whatTimeIsItMrWolf
os.makedirs(comparisonDir)
outputFile = open("Comparison" + whatTimeIsItMrWolf + ".log","w")      
outputFile.write("Listing files and directories recursively under " + input_dir1 + "\n") 
#print "Listing files and directories recursively under ", input_dir1
printAndCompareFiles(input_dir1, input_dir1, input_dir2, comparisonDir, outputFile)
outputFile.close() 
