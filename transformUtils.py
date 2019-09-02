import maya.cmds as cmds
import maya.api.OpenMaya as om2

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
def getmObject(obj1):
    selectList=om2.MSelectionList()
    selectList.add(obj1)
    mObject=selectList.getDependNode(0)
    return mObject

def getPlugByName(mObject,plugName):
    dependNode = om2.MFnDependencyNode(mObject)
    try:
        plugNode = dependNode.findPlug(plugName, 0)
        return plugNode
    except:
        return None
def connectNodes(obj1,obj2,attr1,attr2):
    sourceNode=getmObject(obj1)
    plugNameSrc=getPlugByName(sourceNode,attr1)
    targetNode=getmObject(obj2)
    plugNameTgt=getPlugByName(targetNode,attr2)
    mDGNode=om2.MDGModifier()
    mDGNode.connect(plugNameSrc,plugNameTgt)
    mDGNode.doIt()



