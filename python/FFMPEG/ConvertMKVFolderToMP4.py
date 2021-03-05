# Convert a folder containing a certain file extension to another file extension with FFMPEG

# Variable Examples:
# python CovertMKVFolderToMP4.py VideosToConvert TargetExt ExportExt overwrite batch

# Example:
# python CovertMKVFolderToMP4.py C:/VideosToConvert mkv mp4 y batch
# python "D:\Projects\HoudiniTools\scripts\python\FFMPEG\ConvertMKVFolderToMP4.py" "M:\Projects\VT\VTBITCY01\01-Working\28-JJ\00-Source\01-VIDZ" mkv mp4 y batch
# python "D:\Projects\HoudiniTools\scripts\python\FFMPEG\ConvertMKVFolderToMP4.py" "M:\Projects\VT\VTBITCY01\01-Working\28-JJ\00-Source\01-VIDZ\Video.mkv" mkv mp4 y no

# FFMPEG Command:
# ffmpeg -i filename.mkv -vcodec copy -acodec copy 1.mp4

import os
import subprocess
import sys

folderpath = sys.argv[1]
targetext = sys.argv[2]
exportext = sys.argv[3]
overwrite = sys.argv[4]
batch = sys.argv[5]


def ReadFilesInFolder():
    filestoconvert = []
    for file in os.listdir(folderpath):
        if file.endswith("." + targetext):
            filestoconvert.append(os.path.join(folderpath, file))
    return filestoconvert

def RunCommand(command):
    print("Running Command: " + command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    for line in process.stdout:
        print(line)

def ParseFilename(filename):
    file_name, file_extension = os.path.splitext(filename)
    importfiletext = file_name + "." + targetext
    exportfiletext = file_name + "." + exportext
    return [importfiletext, exportfiletext]

def RunFFMPEGCommand(filetouse):
    # file_name, file_extension = os.path.splitext(filetouse)
    # importfiletext = file_name + "." + targetext
    # exportfiletext = file_name + "." + exportext
    fileinfo = ParseFilename(filetouse)
    
    importfiletext, exportfiletext = fileinfo

    # ffcommand = "ffmpeg -i \"" + importfiletext +"\" -vcodec copy -acodec copy \"" + exportfiletext + "\""
    ffcommand = "ffmpeg -i \"" + importfiletext +"\" \"" + exportfiletext + "\" -y" 
    
    if os.path.exists(exportfiletext):
        if overwrite == "y":
            os.remove(exportfiletext)
            RunCommand(ffcommand)
        else:
            pass
    else:
        RunCommand(ffcommand)
    # process = subprocess.Popen(ffcommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    # for line in process.stdout:
    #     print(line)
        

def ProcessFiles(filesToUse):
    for f in filesToUse:
        RunFFMPEGCommand(f)

# If it's batch
if batch == "batch":
    files = ReadFilesInFolder()
    ProcessFiles(files)
else:
    print("Running Single : " + folderpath)
    fileinfo = ParseFilename(folderpath)
    
    importfiletext, exportfiletext = fileinfo
    # print("importfiletext | " + importfiletext)
    # print("exportfiletext | " + exportfiletext)
    
    RunFFMPEGCommand(folderpath)
    

        