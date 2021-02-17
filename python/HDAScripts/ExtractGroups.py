
        
def GetParentNode(kwargs):
    nodee = kwargs["node"]
    node = kwargs['node']
    nodepath = str(node.name).replace(">>", "")
    return node.path().split(node.name())[0]

def IterateMaterial(kwargs):
    nodee = kwargs["node"]
    material_node = hou.node(nodee.evalParm('Material_Template'))
    num_materials = material_node.evalParm('num_materials')
    matdic = []
    separator = '_'

    for i in range(1,num_materials+1):
        newdic = {"group":"", "mat":""}
        matloc = material_node.parm('shop_materialpath{:d}'.format(i))
        grp = material_node.parm('group{:d}'.format(i))
        # grpsplit = grp.eval().split("_")
        # grpsplit.remove(grpsplit[0])
        # joinedgrp = separator.join(grpsplit)
        # newdic["group"] = joinedgrp
        newdic["group"] = grp
        newdic["mat"] = matloc.eval()
        matdic.append(newdic)
    #print(matdic)
    return matdic
        # grp.set('_'+grp.eval())

def CompareGroupItem(groupname, ToIgnoreArray ):
    
    # print(groupname)
    # print(ToIgnoreArray)
    for matgroup in ToIgnoreArray:
        comparegroup = str(matgroup["group"].eval())
        # print(str(groupname) + " | " +str(matgroup["group"].eval()) )
        if str(groupname) == comparegroup:
            # print(groupname)
            return False
        
    return True
        
def TestButton(kwargs):

    print(GetParentNode(kwargs))
        
def Extract_groups(kwargs):
    nodee = kwargs["node"]
    GroupsToIgnore = IterateMaterial(kwargs)
    
    nodeToCopy = [hou.node(nodee.evalParm('Material_Template'))]
    node = hou.node(nodee.evalParm('Node_To_Split'))
    if nodee.evalParm('Use_FBX_Import') == 1:
        node = hou.node(nodee.evalParm('InternalNode_To_Split'))
    # node = selected_nodes[0]
    geocreated = []
    groups = node.geometry().primGroups()

    objgeo = hou.node('/obj')
    # print(groups)
    for group in groups:
        if CompareGroupItem(group.name(), GroupsToIgnore) == True:
            obj = hou.node('/obj').createNode("geo", group.name())
            output = obj.createNode('output')
            merge = obj.createNode('object_merge')
            merge.parm('objpath1').set(node.path())
            merge.parm('group1').set(group.name())
            if nodee.evalParm('Use_Material_Template') == 1:
                
                thing = hou.copyNodesTo(nodeToCopy,obj)[0]
                thing.setInput(0,merge)
                newnulll = obj.createNode('null', 'null_' +group.name())
                # output.setInput(0,thing)
                newnulll.setInput(0, thing)
                output.setInput(0,newnulll)
                obj.layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
                
                geocreated.append(obj)
            else:
                newnulll = obj.createNode('null', 'null_' +group.name())
                # output.setInput(0,thing)
                newnulll.setInput(0, merge)
                output.setInput(0,newnulll)
                obj.layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
                
                geocreated.append(obj)
    
    networkbox = objgeo.createNetworkBox(groups[0].name())
    networkbox.setComment(groups[0].name())
    hou.node('/obj').layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
    for objj in geocreated:
        networkbox.addItem(objj)
    message = "Succesfullly created : " + str(len(geocreated)) + " object level geometry! All new Geo is located at /obj/";
    
    hou.ui.displayMessage(message,title='Success!')
    
            
def Extract_groupsInternalSeperate(kwargs):
    nodee = kwargs["node"]
    GroupsToIgnore = IterateMaterial(kwargs)
    parentpath = GetParentNode(kwargs)
    nodeToCopy = [hou.node(nodee.evalParm('Material_Template'))]
    node = hou.node(nodee.evalParm('Node_To_Split'))
    if nodee.evalParm('Use_FBX_Import') == 1:
        node = hou.node(nodee.evalParm('InternalNode_To_Split'))
    # node = selected_nodes[0]
    geocreated = []
    filescreated = []
    groups = node.geometry().primGroups()

    objgeo = hou.node(parentpath[:-1])
    
    objparent  = hou.node(parentpath)
    switch = objgeo.createNode('switch')
    geocreated.append(switch)
    
    # print(groups)
    count = 0
    obj = objparent
    for group in groups:
        if CompareGroupItem(group.name(), GroupsToIgnore) == True:
            
            output = obj.createNode('output')
            merge = obj.createNode('object_merge', 'objectmerge_' +group.name())
            merge.parm('objpath1').set(node.path())
            merge.parm('group1').set(group.name())
            if nodee.evalParm('Use_Material_Template') == 1:
                
                thing = hou.copyNodesTo(nodeToCopy,obj)[0]
                thing.setInput(0,merge)
                thing.setName('material_' +group.name())
                newnulll = obj.createNode('null', 'null_' +group.name())
                # output.setInput(0,thing)
                newnulll.setInput(0, thing)
                switch.setInput(count, newnulll)
                count += 1
                geocreated.append(newnulll)
                geocreated.append(merge)
                geocreated.append(thing)
                filescreated.append(thing)
            else:
                                
             
             
                newnulll = obj.createNode('null', 'null_' +group.name())
                # output.setInput(0,thing)
                newnulll.setInput(0, merge)
                switch.setInput(count, newnulll)
                count += 1
                geocreated.append(newnulll)
                geocreated.append(merge)
                filescreated.append(newnulll)
                
    print(objparent)
    obj.layoutChildren(items=(geocreated), horizontal_spacing=2.0, vertical_spacing=-1.0)
    networkbox = objparent.createNetworkBox(groups[0].name())
    networkbox.setComment(groups[0].name())
    # hou.node('/obj').layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
    for objj in geocreated:
        print(objj.name())
        networkbox.addItem(objj)
    message = "Succesfullly created : " + str(len(filescreated)) + " object level geometry! All new Geo is located in the " + groups[0].name() + " subnet";
    
    hou.ui.displayMessage(message,title='Success!')
    
                
def Extract_groupsInternalSubnet(kwargs):
    nodee = kwargs["node"]
    GroupsToIgnore = IterateMaterial(kwargs)
    parentpath = GetParentNode(kwargs)
    nodeToCopy = [hou.node(nodee.evalParm('Material_Template'))]
    node = hou.node(nodee.evalParm('Node_To_Split'))
    if nodee.evalParm('Use_FBX_Import') == 1:
        node = hou.node(nodee.evalParm('InternalNode_To_Split'))
    # node = selected_nodes[0]
    geocreated = []
    filescreated = []
    groups = node.geometry().primGroups()

    objgeo = hou.node(parentpath[:-1])
    
    objparent  = hou.node(parentpath)
    switch = objgeo.createNode('switch')
    geocreated.append(switch)
    output = objgeo.createNode('output')
    output.setInput(0,switch)
    geocreated.append(output)
    
    # print(groups)
    count = 0
    for group in groups:
        if CompareGroupItem(group.name(), GroupsToIgnore) == True:
            obj = objgeo
            merge = obj.createNode('object_merge', 'objectmerge_' +group.name())
            merge.parm('objpath1').set(node.path())
            merge.parm('group1').set(group.name())
            if nodee.evalParm('Use_Material_Template') == 1:
            
                thing = hou.copyNodesTo(nodeToCopy,obj)[0]
                thing.setInput(0,merge)
                thing.setName('material_' +group.name())
                newnulll = obj.createNode('null', 'null_' +group.name())
                newnulll.setInput(0, thing)
                switch.setInput(count, newnulll)
                
                
                count += 1
                geocreated.append(newnulll)
                geocreated.append(merge)
                geocreated.append(thing)
                filescreated.append(thing)
            else:
                            
            
                newnulll = obj.createNode('null', 'null_' +group.name())
                newnulll.setInput(0, merge)
                switch.setInput(count, newnulll)
                
                
                count += 1
                geocreated.append(newnulll)
                geocreated.append(merge)

                filescreated.append(newnulll)
                
    print(objparent)
    hou.node(parentpath).layoutChildren(items=(geocreated), horizontal_spacing=2.0, vertical_spacing=-1.0)
    # networkbox = objparent.createNetworkBox(groups[0].name())
    # networkbox.setComment(groups[0].name())
    # hou.node('/obj').layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
    # for objj in geocreated:
    #     print(objj.name())
    #     networkbox.addItem(objj)
    subnett = hou.node(parentpath).collapseIntoSubnet(geocreated, subnet_name=groups[0].name())
    subnett.moveToGoodPosition(False, False,False, False)
    message = "Succesfullly created : " + str(len(filescreated)) + " object level geometry! All new Geo is located in this Geo Node";
    
    hou.ui.displayMessage(message,title='Success!')
    
    
    
def AddToMultiBlock(kwargs):
    nodee = kwargs["node"]
    
    fileblock = nodee.parm("filecount")
    filepaths = ScanLoadFiles(kwargs)
    
    for i in range(len(filepaths)):
        fileblock.insertMultiParmInstance(i)
        nodee.parm("file_" +str(i + 1)).set(filepaths[i])

        
def ScanLoadFiles(kwargs):
    import glob 
    import os 
    dir_path = os.path.dirname(hou.hipFile.path())
    nodee = kwargs["node"]
    File_Pattern = nodee.parm("File_Pattern").eval().replace("$HIP", dir_path).replace('\\', "/")
    ScanRecursive = nodee.parm("ScanRecursive").eval()
    numb_to_Import = nodee.parm("numb_to_Import").eval()
    recursv = False
    if ScanRecursive == 1:
        recursv = 0
    # The path for listing items
    # The list of items
    files = glob.glob(File_Pattern.replace('\\', "/"))
    sendfiles = []
    for i in range(numb_to_Import):
        sendfiles.append(files[i].replace('\\', "/"))
    return sendfiles
    # print(files)
    
    
           