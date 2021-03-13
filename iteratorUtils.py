import maya.OpenMaya as om
##MItDag doesnt work with open maya 2.

selectList=om.MSelectionList()
dagIter=om.MItDag(om.MItDag.kDepthFirst,om.MFn.kMesh)
while not dagIter.isDone():
    selectList.add(dagIter.fullPathName())
    dagIter.next()
if not selectList.isEmpty():
    om.MGlobal.setActiveSelectionList(selectList)