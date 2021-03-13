import maya.cmds as cmds
import maya.api.OpenMaya as om

def maya_useNewApi():
    pass

class pointOnMeshCommand(om.MPxCommand):
    nodeCreated=False
    positionSpecified=False
    normalSpecified=False
    faceIndexSpecified=False
    relativeSpecified=False
    parameterUSpecified=False
    parameterVSpecified=False
    meshNodeName=""
    pointOnMeshInfoName=""
    faceIndex=-1
    relative=False
    parameterU=0.0
    parameterV=0.0

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return pointOnMeshCommand

    def isUndoable(self):
        return True

    def redoIt(self):
        sList=om.MSelectionList()
        if self.meshNodeName="":
            sList=om.MGlobal.getActiveSelectionList()
            if sList.length()==0:
                raise valueError("no mesh or mesh transform specified")
        else:
            sList.add(meshNodeName)

        meshDagPath=sList.getDagPath(0)

        point=om.MPoint()
        normal=om.MVector()

        if meshDagPath.node().hasFn(om.MFn.kTransform) and meshDagPath.hasFn(om.MFn.kMesh):
            if not self.positionSpecified and not self.normalSpecified:
                self.nodeCreated=True
                meshDagPath.extendToShape()
                dependNode=om.






