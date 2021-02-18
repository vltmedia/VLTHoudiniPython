        
def GetParentNode(kwargs):
    nodee = kwargs["node"]
    node = kwargs['node']
    nodepath = str(node.name).replace(">>", "")
    return node.path().split(node.name())[0]

def FunnelToMops(kwargs):
    parentpath = GetParentNode(kwargs)
    
    objgeo = hou.node(parentpath[:-1])
    
    objparent  = hou.node(parentpath)
    mops = objgeo.createNode('MOPS::Instancer::1.4')
