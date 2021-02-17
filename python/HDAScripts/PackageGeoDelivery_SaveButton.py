

import shutil
import os
import hou
dir_path = os.path.dirname(hou.hipFile.path())

def CopyMaterialSlot(MaterialName,Destination, MaterialSlot , SourceName):
    #print(hou.node("/mat/"+ MaterialName))
    #print("A")
    textureloc = hou.node("/mat/"+ MaterialName).parm(MaterialSlot + "_texture").eval()
    dsetloc = textureloc.replace(SourceName, Destination)
    #print(dsetloc)
    #print("B")
    try:
        shutil.copy(textureloc, dsetloc)
    except IOError as io_err:
        os.makedirs(os.path.dirname(dsetloc))
        shutil.copy(textureloc, dsetloc)

    
def CopyToNewFolder(MaterialName,Destination, SourceName):
    CopyMaterialSlot(MaterialName,Destination,  "basecolor",SourceName)
    CopyMaterialSlot(MaterialName,Destination,  "rough",SourceName)
    CopyMaterialSlot(MaterialName,Destination,  "baseNormal",SourceName)


def SaveFiles(kwargs):
    
    
    node = kwargs['node']
    nodepath = str(node.name).replace(">>", "")
    print(nodepath)
    
    Variation = node.evalParm('Variation')
    
    NamePrefix = str(node.evalParm("Name_Prefix"))
    SaveLocation = str(node.evalParm("Save_Location"))
    UseVariationFolder = node.evalParm("Save_To_Variation_Folders")
    newfolder = SaveLocation+"/" + str(Variation)
    if UseVariationFolder == 0:
        newfolder = SaveLocation
     
    # Set FBX Output Paths    
    newfbx = dir_path + newfolder + "/" +NamePrefix+ str(Variation) + "_LR.fbx"
    newfbxHR = dir_path + newfolder + "/"+NamePrefix + str(Variation) + "_HR.fbx"
    if UseVariationFolder == 0:
        newfbx = dir_path + newfolder + "/" +NamePrefix + "_LR.fbx"
        newfbxHR = dir_path + newfolder + "/"+NamePrefix + "_HR.fbx"
     
    sourceloc =node.evalParm("Texture_Location")

    print(nodepath+"/rop_fbxLR")
    print(hou.node(nodepath+"/rop_fbxLR"))










        
    # message = "Saving to: \n" + newfolder;
    message = "Saving to: \n" + newfbx;
    
    # print(Variation)
    hou.ui.displayMessage(message,title='Super Important Message')