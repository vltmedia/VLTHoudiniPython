def AddToMultiBlock(kwargs):
    nodee = kwargs["node"]
    fileblock = nodee.parm("filecount")
    filepaths = ["../Pop", "C:/Temp/f.fbx",  "C:/Temp/f1.fbx",  "C:/Temp/f2.fbx",  "C:/Temp/f3.fbx",  "C:/Temp/f4.fbx",  "C:/Temp/f5.fbx", ]
    for i in range(len(filepaths)):
        fileblock.insertMultiParmInstance(i)
        nodee.parm("file_" +str(i + 1)).set(filepaths[i])
def AddToMaterialMultiBlock(kwargs):
    nodee = kwargs["node"]
    matblock = nodee.parm("num_materials")
    groups = ["Bubby", "Sanic",  "Gex",  "Mayrio",  "Speero" ]
    filepaths = ["../Pop", "C:/Temp/f.fbx",  "C:/Temp/f1.fbx",  "C:/Temp/f2.fbx" ]
    for i in range(len(filepaths)):
        matblock.insertMultiParmInstance(i)
        nodee.parm("group" +str(i + 1)).set(groups[i])
        nodee.parm("shop_materialpath" +str(i + 1)).set(filepaths[i])
    