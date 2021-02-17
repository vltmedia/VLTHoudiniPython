# This script searches a Folder for a specific file extension, takes the found pictures, parses the filename (needs to be a specific filenaming convention)
# and adds the text on the image. The clean version is then copied to a Temp/cleanfolder folder then the composited image is
# saved in placed of the moved original file.

# File Naming Convention:
# Location-TimeOfDay-Keyword-Version
# Examples:
# StudioA-Day-Interview-01.png
# Interior-Dusk-WindowsillUnderPlant.png

# Arguments: 
# sys.argv[0] = Folder to search
# sys.argv[1] = Extension
# sys.argv[2] = Temp Folder to save the clean files to.

# Example:
# python burninimagename "C:\Pics\Exterior" png "C:\temp"


from PIL import ImageFont, ImageDraw, Image  
import numpy as np
import glob
import cv2
import os
import shutil  
import sys 
import csv  
import re 
      
scriptdir = os.path.dirname(os.path.realpath(__file__))
def camel_case_split(str): 
    words = [[str[0].split(".")[0]]] 

    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c)
    arayyy = [''.join(word) for word in words]
    outword = ' '.join(arayyy)
    return ' '.join(arayyy)
     
def ReadCSV(path):
    csvrows = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            csvrows.append(row)
            
            # if line_count == 0:
            #     print(f'Column names are {", ".join(row)}')
            #     line_count += 1
            # else:
            #     csvrows.append(row)
              
                # line_count += 1
    return csvrows
def WriteCSV(csvpath,csvrows, csvHeaders):
        # name of csv file  
    filename = csvpath
        
    # writing to csv file  
    with open(filename, 'w', newline='') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(csvHeaders)  
            
        # writing the data rows  
        csvwriter.writerows(csvrows)

def checkifFileExists(filename, csvrows):
    found = False
    for file in csvrows:
        try:
            filetofind = filename
            filetocheck = file[7]
            # print(filetofind)
            # print(filetocheck)
            
            if file[7] == filetofind:
                # print(filetofind)
                # print(filetocheck)
                # print("FOUND 2")
                found = True
            
            else:
                if found != True:
                # print(filetofind)
                # print(filetocheck)
                # # print("!!!!!!!!!!!!!!!!!"+filetofind+"!!!!!!!!!!!!!!!!!!!!!!!!")
                # # print("`````````````````"+filetocheck+"`````````````````")
                # print("```FALSE 2```")
                    found = False
        except :
                found = False    
    # print(filetofind)
    # print(filetocheck)
    # print(f"```{found}```")
    return found

def ParseName(Filename):
    outfilename = sys.argv[1] + "/"+Filename
    # print("Parsing Name | " + outfilename)
    img = cv2.imread(outfilename)
        
        # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    dim = str(width) + str(height)
    filenamesplit = filenamee.split("-")
    location = filenamesplit[0]
    timeofday = filenamesplit[1]
    Keyword = camel_case_split(filenamesplit[2])
    
    
    version = ""
    if len(filenamesplit) == 4:
        version = filenamesplit[3].split(".")[0]
    else:
        Keyword = filenamesplit[2].split(".")[0]
    return [filenamee,location,timeofday,  Keyword,version, width, height]
        

def BurnInParsedFilename(filepath, outputfolder, csvrows):
    path = filepath
    
    # path = r'images\Exterior-Dusk-FireEscapeSnow-01.png'
    filenamee = os.path.basename(path)
    # print("Processing: ",filenamee)
    filenameeb = os.path.splitext(filepath)[0]
    filenameeext = os.path.splitext(filepath)[1]
    filenamesplit = filenamee.split("-")
    location = filenamesplit[0]
    timeofday = filenamesplit[1]
    Keyword = camel_case_split(filenamesplit[2])

    
    
    version = ""
    if len(filenamesplit) == 4:
        version = filenamesplit[3].split(".")[0]
    else:
        Keyword = camel_case_split(filenamesplit[2].split(".")[0])
    img = cv2.imread(path)
        
    outfilename = os.path.join( outputfolder,filenamee)
        # height, width, number of channels in image
    height = img.shape[0]
    width = img.shape[1]
    dim = str(width) + str(height)
    # if checkifFileExists(outfilename,csvrows ) == True:
    csvrow = [filenamee,location,timeofday,  Keyword,version, width, height]
    fontpath = scriptdir+ "/built titling sb.ttf"

    # Load an color image in grayscale
    cv2_im_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)  
    pil_im = Image.fromarray(cv2_im_rgb)  
    draw = ImageDraw.Draw(pil_im)  
    # use a truetype font  
    font = ImageFont.truetype(fontpath, 30)  
    # Draw the text  
    draw.text((10, 910), "Location: "+location , font=font, fill=(255,255,255,200))
    draw.text((10, 950),  "TOD: "+timeofday, font=font, fill=(255,255,255,200))
    draw.text((10, 990), "Key: "+ Keyword, font=font, fill=(255,255,255,200))
    draw.text((10, 1030), "Version: "+ version, font=font, fill=(255,255,255,200))
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  
    # cv2.imshow('Fonts', cv2_im_processed)  
    # print(outputfolder)
    # print(os.path.join( outputfolder,filenamee))
    # get dimensions of image
    

    cv2.imwrite(os.path.join( outputfolder,filenamee), cv2_im_processed) 
    return [os.path.join( outputfolder,filenamee), csvrow]
    # else:
    #     csvrow = [filenamee,location,timeofday,  Keyword,version]
        
    #     return [os.path.join( outputfolder,filenamee), csvrow, False]
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def GetFilesInFolder(path):
    return glob.glob(path, recursive=True)
print("0 | ", sys.argv[0])
print("1 | ", sys.argv[1])
print("2 | ", sys.argv[2])
print("3 | ", sys.argv[3])
print("search | ", sys.argv[1]+"\**\*."+sys.argv[2])

usecsv = False
csvread = ["File Name","Location","Timeofday",  "Keyword","Version", "Size" ,  "Preview Image" , "HDR"]    

if os.path.exists(sys.argv[1]+"\meta.csv"):
    usecsv = True
    csvread = ReadCSV(sys.argv[1]+"\meta.csv")




files = GetFilesInFolder(sys.argv[1]+"\**\*."+sys.argv[2]) 

print("files | ", len(files))
# print(files)

tempfolder = r"M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\tex\temps"
tempfolder = sys.argv[3]
cleanfolder = tempfolder+"/cleanbackup"
if os.path.exists(cleanfolder) == False:
    os.makedirs(cleanfolder,True)
# files = GetFilesInFolder(r"M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\tex\HDR\**\*.png")    
csvrows = []
parsed = 0
for file in files:
    filenamee = os.path.basename(file)
    outtempfile = cleanfolder + "/"+os.path.basename(file)
    filepath = file.replace(sys.argv[1],"")
    if checkifFileExists(filepath, csvread) == False:
        print("Writing File | " + filenamee)
        # print(filenamee)
        destfile = BurnInParsedFilename(file, tempfolder, csvread)
        # if destfile[2] == True:
        parsed += 1
        destfile[1].append(file.replace(sys.argv[1],""))
        destfile[1].append(file.replace(sys.argv[1],"").replace(".png", ".hdr"))

        csvrows.append(destfile[1])
        shutil.move(file, os.path.join( cleanfolder, filenamee))  
        
        shutil.move(destfile[0], file)  
        # else:
        #     destfile[1].append(file.replace(sys.argv[1],""))
        #     destfile[1].append(file.replace(sys.argv[1],"").replace(".png", ".hdr"))
        #     csvrows.append(destfile[1])
    else:
        csvroww = ParseName(filepath)
        csvroww.append(filepath.replace(sys.argv[1],""))
        csvroww.append(filepath.replace(sys.argv[1],"").replace(".png", ".hdr"))
        csvrows.append(csvroww)
        
    
    
csvheader = ["File Name","Location","Timeofday",  "Keyword","Version", "Width","Height",  "Preview Image" , "HDR"]    
WriteCSV(sys.argv[1]+"\meta.csv",csvrows,csvheader)
print("Complete! Parsed " + str(parsed) + " files")
# BurnInParsedFilename(files[0], r"M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\tex\temps")