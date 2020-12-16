import maya.cmds as cmds
import maya.mel as mel
import json
from collections import OrderedDict

def removeTimeWarp():
    mel.eval("source sceneTimeWarp;")
    mel.eval("deleteTimeWarp")
    
    try:
        timescale = cmds.getAttr('Velocity_Controller.ts')
        framenum = cmds.getAttr('Velocity_Controller.fc')
        cmds.playbackOptions(maxTime=framenum, animationEndTime = framenum, minTime=0, animationStartTime=0)	
    except:
        timescale = 0.1
    
    cmds.warning("Timewarp Removed")

def applyTimescale(timescale):
    tscale = 1 / timescale
    
    end = cmds.playbackOptions(q=True,max=True)
    
    
    try:
        framenum = cmds.getAttr('Velocity_Controller.fc')
        cmds.playbackOptions(maxTime=framenum * tscale, animationEndTime = framenum * tscale, minTime=0, animationStartTime=0)	
    except:
        print('could not find default frame count')
    
    warp = cmds.timeWarp(g=True, f=[0, end])
    cmds.timeWarp(warp, e=1, mf=(1, end * tscale))

def applyVelo(velo_frames, timescale=1):
    removeTimeWarp()
    
    frames = [None] * len(velo_frames)

    #for i in range(len(velo_frames)):
    #    frames[i] = velo_frames[str(i)] * timescale
    i = 0
    for frame in velo_frames:
        frames[i] = velo_frames[frame] * timescale
        i += 1
    
    warp = cmds.timeWarp(g=True, f=frames)

    cmds.playbackOptions(maxTime=len(velo_frames), animationEndTime=len(velo_frames), minTime=0, animationStartTime=0)	

    for i in range(len(velo_frames)-1):
        cmds.timeWarp(warp, e=1, mf=(i, i))

def __apply_timescale__():
    removeTimeWarp()
    
    try:
        timescale = cmds.getAttr('Velocity_Controller.ts')
    except:
        timescale = 0.1

    applyTimescale(timescale)
    cmds.warning("Timescale set to: " + str(timescale))

def __import__():
    
    veloPath = __importfile_dialog__("VELO Files (*.velo)", "Select Velocity File")

    data = open(veloPath, "r").read()
    velo_frames = json.loads(data, object_pairs_hook=OrderedDict)
    
    try:
        timescale = cmds.getAttr('Velocity_Controller.ts')
    except:
        timescale = 0.1
    
    print(timescale)
    applyVelo(velo_frames, timescale = timescale)
    cmds.warning("Velocity successfully applied")


def __about_window__():
    cmds.confirmDialog(message="Velocity Importer for Maya\n\n- Developed by Airyz and Sheilan\n- Version 1.0.0",
                       button=['OK'], defaultButton='OK', title="About Velocity3D")

def __remove_menu__():
    if cmds.control("VELOMenu", exists=True):
        cmds.deleteUI("VELOMenu", menu=True)
        
def __create_controller__():
    end = cmds.playbackOptions(q=True,max=True)
    
    cmds.spaceLocator(name='Velocity Controller')
    cmds.addAttr( shortName='ts', longName='Timescale', defaultValue=0.5, minValue=0.001, maxValue=1)
    cmds.addAttr( shortName='fc', longName='Framecount', defaultValue=end, minValue=0, maxValue=10000)
    cmds.warning("Velocity Controller Created")
    
def __help__():
    cmds.warning("No Help for you")

def __create_menu__():
    __remove_menu__()

    # Create the base menu object
    cmds.setParent(mel.eval("$tmp = $gMainWindow"))
    menu = cmds.menu("VELOMenu", label="Velo", tearOff=True)

    cmds.menuItem(label="Create Controller", command=lambda x: __create_controller__(
    ), annotation="Creates an object with custom attributes. Used to control timescale")

    cmds.menuItem(label="Import Velo File", command=lambda x: __import__(
    ), annotation="Imports Velocity Data")
    
    cmds.menuItem(label="Apply Timescale", command=lambda x: __apply_timescale__(
    ), annotation="Applies a time warp, slowing the scene down to 10% speed. This is used to render a high framerate playblast to apply your velocity to.")
    
    cmds.menuItem(label="Reset Timewarp", command=lambda x: removeTimeWarp(
    ), annotation="Resets all Timewarping to default")

    cmds.menuItem(label="About", command=lambda x: __about_window__())
    
    cmds.menuItem(label="Help", command=lambda x: __help__(), annotation="Opens a tutorial")


__create_menu__()


def initializePlugin(m_object):
    __create_menu__()
    
    
def uninitializePlugin(m_object):
    __remove_menu__()
