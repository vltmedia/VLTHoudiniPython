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
        grpsplit = grp.eval().split("_")
        grpsplit.remove(grpsplit[0])
        joinedgrp = separator.join(grpsplit)
        newdic["group"] = joinedgrp
        newdic["mat"] = matloc.eval()
        matdic.append(newdic)
    #print(matdic)
    return matdic
        # grp.set('_'+grp.eval())