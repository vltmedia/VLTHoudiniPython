import os
dir_path = os.path.dirname(hou.hipFile.path())

def CheckIfNodeExists(nodename):
    exists = True
    if hou.node(nodename) is None:
        exists = False
    return exists
    

def IterateMaterial(kwargs, nodetocheck):
    nodee = kwargs["node"]
    material_node = nodetocheck
    num_materials = material_node.evalParm('num_materials')
    matdic = []
    separator = '_'

    for i in range(1,num_materials+1):
        newdic = {"group":"", "mat":""}
        matloc = material_node.parm('shop_materialpath{:d}'.format(i))
        grp = material_node.parm('group{:d}'.format(i))
        grpsplit = grp.eval().split("_")
        grpsplit.remove(grpsplit[0])
        joinedgrp = separator.join(grpsplit)
        newdic["group"] = grp
        newdic["mat"] = matloc.eval()
        newdic["newmatname"] = matloc.eval() + "_Octane"
        matdic.append(newdic)
    #print(matdic)
    return matdic
        # grp.set('_'+grp.eval())

def FixHIPPath(path):
    newpath = path.replace(dir_path, "$HIP")
    return newpath

def AddToMaterialMultiBlock(kwargs, MatArray):
    nodee = kwargs["node"]
    matblock = nodee.parm("num_materials")
    matblock.set(0)
    groups = ["Bubby", "Sanic",  "Gex",  "Mayrio",  "Speero" ]
    filepaths = ["../Pop", "C:/Temp/f.fbx",  "C:/Temp/f1.fbx",  "C:/Temp/f2.fbx" ]
    for i in range(len(MatArray)):
        matblock.insertMultiParmInstance(i)
        nodee.parm("group" +str(i + 1)).set(MatArray[i]["group"])
        nodee.parm("shop_materialpath" +str(i + 1)).set(MatArray[i]["material"])

def CleanMatDic(kwargs, MatArray):
    temp = [] 
    res = dict() 
    for key, val in MatArray.items(): 
        if val not in temp: 
            temp.append(val) 
            res[key] = val         
def CleanOldTextures(kwargs, nodetocheck, dic):
    material = hou.node(nodetocheck)
    materialparent = str(nodetocheck).replace(str(material), "")
    materialparentnode = hou.node(materialparent)
    matcheck = hou.node(dic["newmatname"])
    if matcheck is not None:
        matcheck.destroy()
    
    
def ReadMaterialNode(kwargs, nodetocheck, dic):
    # Parse Principled Material
    
    material = hou.node(nodetocheck)
    materialparent = str(nodetocheck).replace(str(material), "")
    materialparentnode = hou.node(materialparent)
    matcheck = hou.node(dic["newmatname"])
    dic["newmatname"].replace(materialparent, "")
    # print("newmatname | "+dic["newmatname"])
    # print( "nodeCheck | "+str(hou.node(nodetocheck)))
    # print( "materialparent | "+materialparent)
    if matcheck is None:
        
        materialstr = str(material)
        
        #Create Octane Mat Node
        octaneNodes = []
        octanematnode = materialparentnode.createNode("octane_vopnet", dic["newmatname"].replace(materialparent, ""))
        octanematnodeOut = hou.node(materialparent  +str(octanematnode) + "/octane_material1")
        UniversalMatNode = octanematnode.createNode("octane::NT_MAT_UNIVERSAL", materialstr + "_Universal")
        octanematnodeOut.setInput(0,UniversalMatNode)
        octaneNodes.append(octanematnodeOut)
        octaneNodes.append(UniversalMatNode)


        # Set Octane Diffuse Texture
        Diffusemode = material.parm("basecolor_useTexture").eval()
        if Diffusemode == 1:
            diffuse = material.parm("basecolor_texture").eval()
            OctaneDiffuseTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneDiffuseTextureNode.parm("A_FILENAME").set(FixHIPPath(diffuse))
            UniversalMatNode.setInput(2,OctaneDiffuseTextureNode)
            octaneNodes.append(OctaneDiffuseTextureNode)
        else:
            UniversalMatNode.parm("albedor").set(material.parm("basecolorr").eval())
            UniversalMatNode.parm("albedog").set(material.parm("basecolorg").eval())
            UniversalMatNode.parm("albedob").set(material.parm("basecolorb").eval())
        

        # Set Octane Rough Texture
        roughmode = material.parm("rough_useTexture").eval()
        if roughmode == 1:
            rough = material.parm("rough_texture").eval()
            OctaneRoughnessTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneRoughnessTextureNode.parm("A_FILENAME").set(FixHIPPath(rough))
            UniversalMatNode.setInput(6,OctaneRoughnessTextureNode)
            octaneNodes.append(OctaneRoughnessTextureNode)
        else:
            UniversalMatNode.parm("roughness").set(material.parm("rough").eval())
            

            
        # Set Octane Normal Texture
        normalmode = material.parm("baseBumpAndNormal_type").eval()
        if normalmode == "normal":
            normal = material.parm("baseNormal_texture").eval()
            OctaneNormalTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneNormalTextureNode.parm("A_FILENAME").set(FixHIPPath(normal))
            UniversalMatNode.setInput(32,OctaneNormalTextureNode)
            octaneNodes.append(OctaneNormalTextureNode)
        if normalmode == "bump":
            normal = material.parm("baseBump_bumpTexture").eval()
            OctaneNormalTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneNormalTextureNode.parm("A_FILENAME").set(FixHIPPath(normal))
            UniversalMatNode.setInput(31,OctaneNormalTextureNode)
            octaneNodes.append(OctaneNormalTextureNode)        

        
        
        # Set Octane Displacement Texture
        displacementmode = material.parm("dispTex_enable").eval()
        if displacementmode == 1:
            displacement = material.parm("dispTex_texture").eval()
            displacementscale = material.parm("dispTex_scale").eval()
            OctaneDisplacementNode = octanematnode.createNode("octane::NT_DISPLACEMENT")
            OctaneDisplacementTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneDisplacementTextureNode.parm("A_FILENAME").set(FixHIPPath(displacement))
            OctaneDisplacementNode.parm("amount").set(displacementscale)
            OctaneDisplacementNode.setInput(0,OctaneDisplacementTextureNode)
            UniversalMatNode.setInput(33,OctaneDisplacementNode)
            octaneNodes.append(OctaneDisplacementTextureNode)
        
            
        # Set Octane Metallic Texture
        metallicmode = material.parm("metallic_useTexture").eval()
        if metallicmode == 1:
            metallictexture = material.parm("metallic_texture").eval()
            OctanemetallictTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctanemetallictTextureNode.parm("A_FILENAME").set(FixHIPPath(metallictexture))
            UniversalMatNode.setInput(3,OctanemetallictTextureNode)
            octaneNodes.append(OctanemetallictTextureNode)
        else:
            UniversalMatNode.parm("metallic").set(material.parm("metallic").eval())   
                
        # Set Octane Opacity Texture
        opacitymode = material.parm("opaccolor_useTexture").eval()
        if opacitymode == 1:
            opacitytexture = material.parm("opaccolor_texture").eval()
            OctaneopacitytTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneopacitytTextureNode.parm("A_FILENAME").set(FixHIPPath(opacitytexture))
            UniversalMatNode.setInput(28,OctaneopacitytTextureNode)
            octaneNodes.append(OctaneopacitytTextureNode)
                    
        # Set Octane Coat Texture
        coatmode = material.parm("coat_useTexture").eval()
        if coatmode == 1:
            coattexture = material.parm("coat_texture").eval()
            OctanecoattTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctanecoattTextureNode.parm("A_FILENAME").set(FixHIPPath(coattexture))
            UniversalMatNode.setInput(15,OctanecoattTextureNode)
            octaneNodes.append(OctanecoattTextureNode)
                    
        # Set Octane Coat Rough Texture
        coatroughmode = material.parm("coatrough_useTexture").eval()
        if coatroughmode == 1:
            coatroughtexture = material.parm("coatrough_texture").eval()
            OctanecoatroughtTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctanecoatroughtTextureNode.parm("A_FILENAME").set(FixHIPPath(coatroughtexture))
            UniversalMatNode.setInput(16,OctanecoatroughtTextureNode)
            octaneNodes.append(OctanecoatroughtTextureNode)
                    
        # Set Octane IOR Texture
        iormode = material.parm("ior_useTexture").eval()
        if iormode == 1:
            iortexture = material.parm("ior_texture").eval()
            OctaneiortTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneiortTextureNode.parm("A_FILENAME").set(FixHIPPath(iortexture))
            UniversalMatNode.setInput(21,OctaneiortTextureNode)
            octaneNodes.append(OctaneiortTextureNode)
        
                        
        # Set Octane Anistropy Texture
        anisomode = material.parm("aniso_useTexture").eval()
        if anisomode == 1:
            anisotexture = material.parm("aniso_texture").eval()
            OctaneanisotTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneanisotTextureNode.parm("A_FILENAME").set(FixHIPPath(anisotexture))
            UniversalMatNode.setInput(7,OctaneanisotTextureNode)
            octaneNodes.append(OctaneanisotTextureNode)
        
                            
        # Set Octane Dispersion Texture
        dispersionmode = material.parm("dispersion_useTexture").eval()
        if dispersionmode == 1:
            dispersiontexture = material.parm("dispersion_texture").eval()
            OctanedispersiontTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctanedispersiontTextureNode.parm("A_FILENAME").set(FixHIPPath(dispersiontexture))
            UniversalMatNode.setInput(26,OctanedispersiontTextureNode)
            octaneNodes.append(OctanedispersiontTextureNode)
        
        
        
                
        # Set Octane Emission Texture
        emissionmode = material.parm("emitcolor_useTexture").eval()
        if emissionmode == 1:
            emissiontexture = material.parm("emitcolor_texture").eval()
            emissionamount = material.parm("emitint").eval()
            OctaneemissiontNode = octanematnode.createNode("octane::NT_EMIS_TEXTURE")
            OctaneemissiontTextureNode = octanematnode.createNode("octane::NT_TEX_IMAGE")
            OctaneemissiontTextureNode.parm("A_FILENAME").set(FixHIPPath(emissiontexture))
            OctaneemissiontTextureNode.parm("power").set(emissionamount)
            OctaneemissiontNode.setInput(0,OctaneemissiontTextureNode)
            UniversalMatNode.setInput(36,OctaneemissiontNode)
            octaneNodes.append(OctaneemissiontTextureNode)
        
        

        
        # Cleanup Octane Mat Layout
        octanematnode.moveToGoodPosition(False, False,False, False)
        octanematnode.layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
        
        return(materialparent  +str(octanematnode))
    
    
    else:
    
        return(materialparent  +str(matcheck))
    
    
def ReadCurrentMaterial(kwargs):
    node = kwargs["node"]
    inputgeo = node.input(0)
    matnodes = IterateMaterial(kwargs, inputgeo)
    octanematInfo = []
    
    for i in range(len(matnodes)):
        CleanOldTextures(kwargs, matnodes[i]["mat"], matnodes[i] )
        
    for i in range(len(matnodes)):
    # for i in range(2):
        matdic = {"group":"", "material": ""}
        octanemat = ReadMaterialNode(kwargs, matnodes[i]["mat"], matnodes[i])
        groupname = str(matnodes[i]["group"].eval())
        matdic["group"] = groupname
        matdic["material"] = octanemat
        octanematInfo.append(matdic)
    AddToMaterialMultiBlock(kwargs, octanematInfo)
