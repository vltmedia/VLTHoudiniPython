# Apply Subdivide SOP Verb
import glob
import hou
import os 
import random 
dir_path = os.path.dirname(hou.hipFile.path())
node = hou.pwd()

def TimeNodeInitialize(kwargs, timenode):
    node = kwargs['node']
    TimeOffsetRangee = [int(node.evalParm('Time_Offset_Random_Rangemin')),int(node.evalParm('Time_Offset_Random_Rangemax'))]
    Time_Offset = int(node.evalParm('Time_Offset'))
    timetext = random.randrange(TimeOffsetRangee[0], TimeOffsetRangee[1]) + Time_Offset
    
    preset = {
                "frame": "`$F` + " + str(timetext) ,
                "rangeclamp": 3
            }

    node = kwargs['node']
    
    # timenode.parm("frame").set(timetext )
    timerange = hou.playbar.timelineRange()
    firstframe = timerange[0] + timetext
    lastframe = timerange[1] + timetext
    timenode.parm('frange1').deleteAllKeyframes()
    timenode.parm('frange2').deleteAllKeyframes()
    timenode.parm('frame').deleteAllKeyframes()
    timenode.parm('frame').setExpression("$F + "+ str(timetext), hou.exprLanguage.Hscript)
    timenode.parm('frange1').setExpression(str(firstframe), hou.exprLanguage.Hscript)
    timenode.parm('frange2').setExpression(str(lastframe), hou.exprLanguage.Hscript)
    timenode.parm("rangeclamp").set(3)
    # timenode.setParms(preset)
def ReseedTimes(kwargs):
    node = kwargs['node']
    generated = node.evalParm('Generated')
    if generated == 1:
        generatednode = hou.node(node.evalParm('Generated_Subnet'))
        try:
            generatednode.destroy()
        except :
            p = 0
    RunImportfiles(kwargs)
        

def RunCheckMatchCount(kwargs):
    node = kwargs['node']
    parentnode = node.parent()
    grandparentnode = parentnode
    global dir_path

    subnetnode = node
    generatedNodes = []

    filepatternConverted = node.evalParm('File_Pattern')

    filess = glob.glob(filepatternConverted)
    node.parm('Match_Count').set(str(len(filess)))
    node.parm('Generated_Count').set(1)
    
        
def RunImportfiles(kwargs):
    node = kwargs['node']
    parentnode = node.parent()
    grandparentnode = parentnode
    global dir_path
    mergenode = parentnode.createNode("merge")

    subnetnode = node
    generatedNodes = []
    importfilestoggle = node.parm('Import_Files')

    Import_Range = [int(node.evalParm('Import_Rangemin')),int(node.evalParm('Import_Rangemax'))]
    TimeOffsetRange = [node.evalParm('Time_Offset_Random_Rangemin'),node.evalParm('Time_Offset_Random_Rangemax')]
    ResultingSubnetName = node.evalParm('Resulting_Subnet_Name')
    filepatternConverted = node.evalParm('File_Pattern')
    Merge_Subnet_With_Other_Subnets = node.evalParm('Merge_Subnet_With_Other_Subnets')
    Subnets_Merge_Node = node.evalParm('Subnets_Merge_Node')
    filepattern = node.parm('File_Pattern').rawValue()
    filepatternhip = node.parm('File_Pattern').rawValue()

    copynodes = node.evalParm('Nodes_To_Copy').split(' ')
    nodestocopy = []

    for  i in range(0, len(copynodes)):
        nodestocopy.append(hou.node(copynodes[i]))
    # searchfilepattern = node.evalParm('File_Pattern')


    # print(filepattern)
    filenamesplitHip = filepattern.replace("`$HIP`", hou.hipFile.path()).split('*')
    filenamesplit = filepatternConverted.replace("`$HIP`", hou.hipFile.path()).split('*')
    # print(filepatternConverted.replace("`$HIP`", hou.hipFile.path()).split('*'))

    filess = glob.glob(filepatternConverted)

    # print(filess[2].replace(filenamesplit[len(filenamesplit)-1],filenamesplitHip[len(filenamesplitHip)-1]))
    # print (len(filess))
    # print (copynodes)
    # print (nodestocopy)


    # createdtemplatecopies = hou.copyNodesTo(nodestocopy, parentnode)

    # for i in range(0, 4):
    # for i in range(0, len(filess) - 1 ):
    for  i in range(Import_Range[0], Import_Range[1]):

        try:

            # CreateSetImportNode(filess[i],i)
            fileimportnode = parentnode.createNode("file" )
            timeshiftnode = parentnode.createNode("timeshift" )
            # timeshiftnode.parm('frame').setExpression("```$F``` + 3", hou.exprLanguage.Hscript)

            # print(timeshiftnode.evalParm('frame'))
            TimeNodeInitialize(kwargs,timeshiftnode )
            fileimportnode.parm('file').set(filess[i].replace(filenamesplit[len(filenamesplit)-1],filenamesplitHip[len(filenamesplitHip)-1]))
            templates = []
            try:
                templates = hou.copyNodesTo(nodestocopy,parentnode)
                timeshiftnode.setInput(0,fileimportnode, 0)
            
                templates[0].setInput(0,timeshiftnode, 0)
                
                mergenode.setInput(i,templates[len(templates) - 1], 0)
                for nodeee in templates:
                    generatedNodes.append(nodeee)
                generatedNodes.append(fileimportnode)
                generatedNodes.append(timeshiftnode)
            except :
            
                
                timeshiftnode.setInput(0,fileimportnode, 0)
                mergenode.setInput(i,timeshiftnode, 0)

                generatedNodes.append(fileimportnode)
                generatedNodes.append(timeshiftnode)
        except:
            print("Index doesn't exist | ", i)
        
    mergenodename = mergenode.name()
    generatedNodes.append(mergenode)
    subnetnode = parentnode.collapseIntoSubnet(generatedNodes, ResultingSubnetName.replace(" ", "_"))
    mergenode = hou.node(subnetnode.path() +"/"+  mergenodename)
    subnetoutputnode = subnetnode.createNode("output" )
    subnetoutputnode.setInput(0,mergenode, 0)
    node.parm('Generated_Subnet').set(subnetnode.path())
    node.parm('Generated').set(1)
    if Merge_Subnet_With_Other_Subnets == 1:
        Subnets_Merge_Nodee = hou.node(Subnets_Merge_Node)
        Subnets_Merge_Nodee.setInput(len(Subnets_Merge_Nodee.inputs()),subnetnode,0 )
    subnetnode.layoutChildren(items=(), horizontal_spacing=2.0, vertical_spacing=-1.0)
    hou.ui.displayMessage('Successfully created Import Subnet! | ' + subnetnode.path(),title='Success! ')
    # resetToggle(importfilestoggle)

def resetToggle(importfilestoggle):
    if node.evalParm('Import_Files') == 1:
        importfilestoggle.set(0) 
#print('search File pattern | ', searchfilepattern)

def CreateSetImportNode(filepath, indexx):
    global node
    global parentnode
    global grandparentnode
    global generatedNodes
    global mergenode
    fileimportnode = grandparentnode.createNode("file" )
    fileimportnode.parm('file').set(filepath)
    templates = hou.copyNodesTo(nodestocopy,grandparentnode)
    templates[0].setInput(0,fileimportnode, 0)
    mergenode.setInput(indexx,templates[1], 0)
    for nodeee in templates:
        generatedNodes.append(nodeee)
    generatedNodes.append(fileimportnode)
    




