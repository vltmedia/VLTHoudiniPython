# Executes a Python script, either in process or as a job
#
# The following variables and functions are available in both case:
# work_item
# intData, floatData, strData,
# intDataArray, floatDataArray, strDataArray
#
# In addition to the above, in-process scripts can also access:
# self         - the current PDG node
# parent_item  - the parent work item, if it exists
import subprocess
import os
source = "M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/Testing/HDR - Original"

temp = "M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/temp"
sourcefix = source.replace(' ', '/ ')
tempfix = temp.replace(' ', '/ ')
# cmd = '"M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/burnimagesNames.bat" png "M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/Testing/HDR - Original" "M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/Testing/temp"'.split()
cmd2 = ["M:/Projects/Sketches/ScifiSketches/01-Working/28-JJ/04-3D/Scifi-Kitbash/ScifiKitbash/scripts/python/image/burnimagesNames-Args.bat", source,  "png", temp]
# os.system(cmd2)
process = subprocess.Popen(cmd2,  shell=True)

# subprocess.call(cmd)