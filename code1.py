import maya.api.OpenMaya as om2

##get the full dagpath for all selected object.
# use partialPathName if u just want the name of the selection

dagPathEle = []
selList = om2.MGlobal.getActiveSelectionList()
for i in range(selList.length()):
	dagPath = selList.getDagPath(i)
	dagPathEle.append(dagPath.partialPathName())

print dagPathEle


