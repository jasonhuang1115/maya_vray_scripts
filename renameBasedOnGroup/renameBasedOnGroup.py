import maya.cmds as cmds

# Based on user selection, the script will reanme a mesh based on its parent group node.
# selection scenario 1: a group that contains multiple child groups and meshes. The script will travel down to each child mesh
#  node and rename the mesh based on its parent group name. (ex. parent group name is hood. child mesh name is gonna be hood1, hood2, etc..
# selection scenario 2: a group contains multiple meshes. The script will travel down the hierarchy to each mesh node and rename the mesh
# based on its parent group's name
# selection scenario 3: a single or multiple meshes. The script will find each meshes parent group and rename accordingly.

# rename the transfrom node as well as the shape node (shape node seems to be renamed automatlly when the transform node is renamed)

## update 05-03-2018: need to catch some outliers:
##    1) when a transform node is selected, currently the script renames the mesh node it is associated with but not the transform node
##       itself based on its parent.

# make sure the user make a selection in the scene
selection = cmds.ls(selection=True, shapes=False)
if not selection:
    raise StandardError('nothing is selected in the scene. Select an mesh or group to start with')
print '#1 selection: current user selection is ', selection


# store a dictionary that stores lists of mesh nodes and their corresponding immediate parent group as the keys
#selectedNodes = []
selectedNodes = cmds.ls(selection=True, long=True)
print '#2 selectedNodes: user selection as a list: ', selectedNodes

# get the children of selected nodes
nodesList = cmds.listRelatives(selectedNodes, fullPath=True, children=True)
print '#3 nodesList: children of selectedNodes as a list: ', nodesList

# catch if user slection only contains an empty group or multiple empty groups and rename these groups accordingly
if nodesList == None:
    print '#3.1 nodeList is a None. i.e. there is no child for the selected node.'
    # first filter to catch outliers: Here we try to catch if selected nodes contains mesh nodes
    for each in selectedNodes:
        print '#3.2 node being iterated in selectedNodes ', each
        if cmds.nodeType(each) == 'mesh':
            print '#3.3 selected node is mesh'
            nodesList = selectedNodes
            print '#3.4 nodesList: due to nodeList is a None, it is reassigned to selectedNode: ', selectedNodes
        else:
            print '#3.5 selected node(s) is an empty group(s)'
            # groupEval(each)
            parent = cmds.ls(each, long=True)[0].split('|')[-2]
            cmds.rename(each, parent+'_emptyGRP1')


def is_group(node):
    print '#7 the node that is passed into is_group function: ', node

    children = []
    if cmds.nodeType(node) == 'mesh':
        print '#7.1 node evaluated by is_group function is a mesh'
        # rename the mesh based on its parent group. If no parent group, return a message in script editor.
        return False

    if cmds.nodeType(node) != 'transform':
        print '#7.2 selected node is not a transform node: ', node
        #raise StandardError('for now, raise an error. Later rename the selection based on its parent group')
        
    children = cmds.listRelatives(node, fullPath=True, children=True)
    
    if children == None:
        print '#7.3 selected node has no child node'
        return True

    for c in children:
        # this is to catch if there is a contraint node in the group
        if cmds.nodeType(c) == 'parentConstraint':
            return True
        if cmds.nodeType(c) != 'transform':
            print '#7.4 the node has a child that is not a transform node. Return False for is_group'
            
            return False
            #raise StandardError('for now, raise an error. Later rename the selection based on its parent group')
    else:
        print '#7.5 The selected node is a group and the last node being evaluated in the selected node\'s hierarchy is: ', c        
        print '#7.6 nodes inside selected group as a list = ', children        
        return True

# define a function to decide what to do when the parsed node is and is not a group. 
def groupEval(nodesSelected, nodes):
    print '#4 selectedNodes that is passed into groupEval function is: ', nodesSelected
    print '#4.1 the childern of selectedNodes (nodesList) that is passed into groupEval fucntion: ', nodes

    # catch outliers
    if nodes == None:
        print '#4.3 selectedNodes that is passed into groupEval function is: ', nodesSelected
        print '#4.4 nodes being evaluated in groupEval function is a None. Nodes = ', nodes
        # parent = cmds.ls(nodesSelected, long=True)[0].split('|')[-2]
        # print '#4.3 parent of the None nodes being evaluated is: ', parent
        # cmds.rename(nodes, parent+'_emptyGRP1')
    else:
        for single in nodesSelected:
            if is_group(single):
                nodesInTheGroup = []
                for eachNode in nodes:
                    if is_group(eachNode):    
                        print '#5', eachNode, 'is a group.'
                        nodesInTheGroup = cmds.listRelatives(eachNode, fullPath=True, children=True)
                        print '#5.1 children of the group are', nodesInTheGroup
                        if nodesInTheGroup == None:
                            print '#5.3 nodesInTheGroup is a None'
                            parent = cmds.ls(eachNode, long=True)[0].split('|')[-2]
                            print '#5.4 parent of None is: ', parent
                            cmds.rename(eachNode, parent+'_emptyGRP1')

                        else:
                            groupEval(nodesSelected, nodesInTheGroup)
                        
                    else:
                        # grab immediate parent of the selected node
                        print '#6 is_group returns False. User selection is: ', selection

                        if cmds.nodeType(selection) == 'mesh':
                            print '#6.1 selection is mesh'
                            parentTransform = cmds.ls(eachNode, long=True)[0].split('|')[-2]    
                            parent = cmds.ls(eachNode, long=True)[0].split('|')[-3]
                            cmds.rename(parentTransform, parent+'_mesh1')
                        # elif cmds.nodeType(selection) == 'transform':
                        #     print '#6.2 selection is a transform'
                        #     parent = cmds.ls(eachNode, long=True)[0].split('|')[-2]
                        #     cmds.rename(selection, parent+'_mesh1')
                        else:
                            parent = cmds.ls(eachNode, long=True)[0].split('|')[-2]
                            #parent = cmds.ls(selection, long=True)[0].split('|')[-1]
                            print '#6.2', eachNode, 'is a mesh. The immediate parent of', eachNode, "is", parent
                            cmds.rename(eachNode, parent+'_mesh1')
            elif cmds.nodeType(single) == 'mesh':
                parentTransform = cmds.ls(single, long=True)[0].split('|')[-2]    
                parent = cmds.ls(single, long=True)[0].split('|')[-3]
                cmds.rename(parentTransform, parent+'_mesh1')
            else:
                parent = cmds.ls(single, long=True)[0].split('|')[-2]
                cmds.rename(single, parent+'_mesh1')

                    

print '#22 selectedNodes: user selection as a list: ', selectedNodes
print '#33 nodesList: children of selectedNodes as a list: ', nodesList

groupEval(selectedNodes, nodesList)










