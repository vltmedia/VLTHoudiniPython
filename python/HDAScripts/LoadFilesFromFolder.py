
def ScanLoadFiles(kwargs):
    import glob 
    import os 
    dir_path = os.path.dirname(hou.hipFile.path())
    nodee = kwargs["node"]
    File_Pattern = nodee.parm("File_Pattern").eval().replace("$HIP", dir_path)
    ScanRecursive = nodee.parm("ScanRecursive").eval()
    recursv = False
    if ScanRecursive == 1:
        recursv = 0
    # The path for listing items
    # The list of items
    files = glob.glob(File_Pattern)
    return files
    # print(files)
    