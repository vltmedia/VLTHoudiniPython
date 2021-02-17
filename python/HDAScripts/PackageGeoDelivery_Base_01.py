import shutil
import os
node = hou.pwd()
geo = node.geometry()
dir_path = os.path.dirname(hou.hipFile.path())
RenderDoneNode = hou.node("../").parm("RenderDone")




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

def main():    

    Variation = str(hou.node("../").parm("Variation").eval())
    NamePrefix = str(hou.node("../").parm("Name_Prefix").eval())
    SaveLocation = str(hou.node("../").parm("Save_Location").eval())
    newfolder = SaveLocation+"/" + Variation
    if hou.node("../").parm("Variation").eval() == 0:
        newfolder = SaveLocation
        
    # Set FBX Output Paths    
    newfbx = dir_path + newfolder + "/" +NamePrefix+ Variation + "_LR.fbx"
    newfbxHR = dir_path + newfolder + "/"+NamePrefix + Variation + "_HR.fbx"

    sourceloc = hou.node("../").parm("Texture_Location").eval()

    hou.node("../rop_fbxLR").parm("sopoutput").set(newfbx)
    hou.node("../rop_fbxHR").parm("sopoutput").set(newfbxHR)
    hou.node("../rop_fbxHR").parm("execute").pressButton()
    hou.node("../rop_fbxLR").parm("execute").pressButton()
    RenderDoneNode.set(1)



    CopyToNewFolder("Stalks", newfolder, sourceloc)
    CopyToNewFolder("Raddish", newfolder, sourceloc)
    CopyToNewFolder("Roots", newfolder, sourceloc)
    print("Done!")
    
RenderDone = RenderDoneNode.eval()
print(RenderDone)
if RenderDone == 0:
    main()
else:
    print("Already Rendered")