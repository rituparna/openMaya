import maya.cmds as cmds
import maya.api.om2 as om2
import sys
import math

##creating empty dag nodes
#test = createEmptyNodes('test', 8)

def createEmptyNodes(prefixB='', number=4):
    mdagMod = om2.MDagModifier()
    dagArray = []
    for i in range(number):
        dagMod = mdagMod.createNode('transform')
        mdagMod.renameNode(dagMod, '{}{:02d}'.format(prefixB, i))
        dagArray.append(dagMod)
    for i, each in enumerate(dagArray):
        if i < (len(dagArray) - 1):
            mdagMod.reparentNode(dagArray[i + 1], each)
    mdagMod.doIt()


##DGModifier connect
#transformUtils.connectNodes('pCube1','pSphere1','translateX','translateZ')
def getMDagPath(node):
    selList = om2.MSelectionList()
    selList.add(node)
    return selList.getDagPath(0)


def getMObject(node):
    selList = om2.MSelectionList()
    selList.add(node)
    return selList.getDependNode(0)

def getPlugByName(mObject,plugName):
    dependNode = om2.MFnDependencyNode(mObject)
    try:
        plugNode = dependNode.findPlug(plugName, 0)
        return plugNode
    except:
        return None
def connectNodes(obj1,obj2,attr1,attr2):
    sourceNode=getMObject(obj1)
    plugNameSrc=getPlugByName(sourceNode,attr1)
    targetNode=getMObject(obj2)
    plugNameTgt=getPlugByName(targetNode,attr2)
    mDGNode=om2.MDGModifier()
    mDGNode.connect(plugNameSrc,plugNameTgt)
    mDGNode.doIt()

def get_worldMatrixData_inverse(obj):
    # get world matrix data and inverse position
    default_obj = om2.MGlobal.getSelectionListByName(obj)
    default_node = default_obj.getDependNode(0)
    depend_node = om2.MFnDependencyNode(default_node)

    mat_plug = om2.MPlug(depend_node.findPlug('worldMatrix', 0))

    mat_plug = mat_plug.elementByLogicalIndex(0)
    mat_plug = mat_plug.asMObject()

    matData = om2.MFnMatrixData(mat_plug).matrix()
    new_data = matData.inverse()

    trans_matrix = om2.MTransformationMatrix(new_data)
    new_trans = trans_matrix.translation(om2.MSpace.kWorld)
    trans_node = om2.MFnTransform(default_node)
    trans_node.setTranslation(new_trans, om2.MSpace.kTransform)

def matchTranformation(targetNode, followerNode, translation=True, rotation=True):
    followerMTransform = om2.MFnTransform(getMDagPath(followerNode))
    targetMTransform = om2.MFnTransform(getMDagPath(targetNode))
    targetMTMatrix = om2.MTransformationMatrix(om2.MMatrix(cmds.xform(targetNode, matrix=True, ws=1, q=True)))
    if translation:
        targetRotatePivot = om2.MVector(targetMTransform.rotatePivot(om2.MSpace.kWorld))
        followerMTransform.setTranslation(targetRotatePivot, om2.MSpace.kWorld)
    if rotation:
        # using the target matrix decomposition
        # Worked on all cases tested
        followerMTransform.setRotation(targetMTMatrix.rotation(True), om2.MSpace.kWorld)

        # Using the MFnTransform quaternion rotation in world space
        # Doesn't work when there is a -1 scale on the object itself
        # Doesn't work when the object has frozen transformations and there is a -1 scale on a parent group.
        # followerMTransform.setRotation(MFntMainNode.rotation(om2.MSpace.kWorld, asQuaternion=True),om2.MSpace.kWorld)

def getMatrix(node):
    '''
    Gets the world matrix of an object based on name.
    '''
    # Selection list object and MObject for our matrix
    selection = om2.MSelectionList()
    matrixObject = om2.MObject()

    # Adding object
    selection.add(node)

    # New api is nice since it will just return an MObject instead of taking two arguments.
    MObjectA = selection.getDependNode(0)

    # Dependency node so we can get the worldMatrix attribute
    fnThisNode = om2.MFnDependencyNode(MObjectA)

    # Get it's world matrix plug
    worldMatrixAttr = fnThisNode.attribute("worldMatrix")

    # Getting mPlug by plugging in our MObject and attribute
    matrixPlug = om2.MPlug(MObjectA, worldMatrixAttr)
    matrixPlug = matrixPlug.elementByLogicalIndex(0)

    # Get matrix plug as MObject so we can get it's data.
    matrixObject = matrixPlug.asMObject()

    # Finally get the data
    worldMatrixData = om2.MFnMatrixData(matrixObject)
    worldMatrix = worldMatrixData.matrix()

    return worldMatrix


def decompMatrix(node, matrix):
    '''
    Decomposes a MMatrix in new api. Returns an list of translation,rotation,scale in world space.
    '''
    # Rotate order of object
    rotOrder = cmds.getAttr('%s.rotateOrder' % node)

    # Puts matrix into transformation matrix
    mTransformMtx = om2.MTransformationMatrix(matrix)

    # Translation Values
    trans = mTransformMtx.translation(om2.MSpace.kWorld)

    # Euler rotation value in radians
    eulerRot = mTransformMtx.rotation()

    # Reorder rotation order based on ctrl.
    eulerRot.reorderIt(rotOrder)

    # Find degrees
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

    # Find world scale of our object.
    scale = mTransformMtx.scale(om2.MSpace.kWorld)

    # Return Values
    return [trans.x, trans.y, trans.z], angles, scale


# If we're in the main namespace run our stuffs!
if __name__ == '__main__':
    # Defining object name.
    nodeName = 'yourName'

    # Get Matrix
    mat = getMatrix(nodeName)

    # Decompose matrix
    matDecomp = decompMatrix(nodeName, mat)

    # Print our values
    sys.stdout.write('\n---------------------------%s---------------------------\n' % nodeName)
    sys.stdout.write('\nTranslation : %s' % matDecomp[0])
    sys.stdout.write('\nRotation    : %s' % matDecomp[1])
    sys.stdout.write('\nScale       : %s\n' % matDecomp[2])



