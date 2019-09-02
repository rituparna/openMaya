#create joint chain
import maya.cmds as cmds
import maya.api.OpenMaya  as om2

##creating joint chain with offset in x axis
##execute example
#run=jointCreate(5,.8)
def jointCreate(numJoint,offsetValueX):
    jntChain=[]
    initPos=0
    for i in range(numJoint):
        jnt=cmds.createNode('joint',n='testChain{:02d}_jnt'.format(i))
        cmds.xform(jnt,t=(initPos,0,0),a=1)
        initPos+=offsetValueX
        jntChain.append(jnt)
    for i,each in enumerate(jntChain):
        if i<(len(jntChain)-1):
            cmds.parent(jntChain[i+1],each)



