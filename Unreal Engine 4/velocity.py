import unreal 
import json
from collections import OrderedDict
import os
#UI Stuff
import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

def createNewLevelSequence(dest, name):
    return unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name = name, package_path = dest, asset_class = unreal.LevelSequence, factory=unreal.LevelSequenceFactoryNew())

def addVideoCut(track, seq_asset):
    section = track.add_section()
    section.set_editor_property('sub_sequence', seq_asset)
    return section

file_path = tkFileDialog.askopenfilename()

with open(file_path) as json_file:
    data = json.load(json_file, object_pairs_hook=OrderedDict)

    file_name = os.path.splitext(file_path)[0].split('/')[-1].replace(' ', '_')

    utility_library = unreal.EditorUtilityLibrary
    seq_asset = utility_library.get_selected_assets()[0]

    #Get Selected Asset
    assetName = seq_asset.get_name()
    assetPath = seq_asset.get_path_name()[:-(len(assetName)*2+2)]

    #Create new sequence and add the original as a sub sequence
    master_sequence = createNewLevelSequence(assetPath, assetName + "_" + file_name + "_")
    shotsTrack = master_sequence.add_master_track(unreal.MovieSceneCinematicShotTrack)
    timescaleTrack = master_sequence.add_master_track(unreal.MovieSceneSlomoTrack)
    timescale_channel = timescaleTrack.add_section().get_channels()[0]
    section = addVideoCut(shotsTrack, seq_asset)
    section.set_end_frame(seq_asset.get_playback_end())

    first_frame = list(data.values())[0]

    time_dilation = 0
    length = len(data)
    last_time = first_frame

    #Loop through all keys
    for i in range(length - 1):
        key_time = last_time + time_dilation
        last_time = key_time

        #Calculate the required time dilation and set key
        time_dilation = data[list(data.keys())[i + 1]] - data[list(data.keys())[i]]
        timescale_channel.add_key(unreal.FrameNumber(key_time), time_dilation)
    
    end_time = last_time + (time_dilation * 2)

    #Set start and end time
    master_sequence.set_playback_start(first_frame)
    master_sequence.set_playback_end(end_time)
