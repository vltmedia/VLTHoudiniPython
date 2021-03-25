import os
import hou
dir_path = os.path.dirname(hou.hipFile.path())

octaneexrpath = "/topnet1/ropfetch7"
octanepngpath = "/topnet1/ropfetch13"
wedge3path = "/topnet1/wedge3"
csvoutput1path = "/topnet1/csvoutput1"
topnetpath = "/topnet1"
output0path = "/output0"

def CheckIfNodeExists(nodename):
    exists = True
    if hou.node(nodename) is None:
        exists = False
    return exists
    
def GetParentNode(kwargs):
    nodee = kwargs["node"]
    node = kwargs['node']
    nodepath = str(node.name).replace(">>", "")
    return node.path().split(node.name())[0]

def RunTopNode(path):
    top_node = hou.node(path)
    try:
        top_node.generateStaticItems(True)
        top_node.cook(True)
        
    except :
        print("No WorkItems to Generate")
    top_node.executeGraph()
    

def GetParentPath(kwargs):
    parentpath = GetParentNode(kwargs)
    
    objgeo = hou.node(parentpath[:-1])
    
    objparent  = hou.node(parentpath)
    return parentpath
    # mops = objgeo.createNode('MOPS::Instancer::1.4')
    
def RunHDRIRenderExr(kwargs):
    global octaneexrpath
    global octanepngpath
    global wedge3path
    global topnetpath
    global csvoutput1path
    global output0path
    node = kwargs["node"]
    inputgeo = node.input(0)
    fullpath = GetParentPath(kwargs) +  node.name()
    octaneexrpath = fullpath +  octaneexrpath
    octanepngpath = fullpath +  octanepngpath
    wedge3path = fullpath +  wedge3path
    topnetpath = fullpath +  topnetpath
    output0path = fullpath +  output0path
    csvoutput1path = fullpath +  csvoutput1path
    print(octaneexrpath)
    RunTopNode(octaneexrpath)
    
def RunHDRIRenderPNG(kwargs):
    global octaneexrpath
    global octanepngpath
    global wedge3path
    global topnetpath
    global csvoutput1path
    global output0path
    node = kwargs["node"]
    inputgeo = node.input(0)
    fullpath = GetParentPath(kwargs) +  node.name()
    octaneexrpath = fullpath +  octaneexrpath
    octanepngpath = fullpath +  octanepngpath
    wedge3path = fullpath +  wedge3path
    topnetpath = fullpath +  topnetpath
    output0path = fullpath +  output0path
    csvoutput1path = fullpath +  csvoutput1path
    print(octanepngpath)
    RunTopNode(octanepngpath)
